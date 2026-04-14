"""Entity Memory — knowledge graph for cross-session memory.

Three tiers of memory in spider.Web:
  1. Working Memory: conversation buffer (50 messages, per-session)
  2. Episodic Memory: RAG vector search (SQLite, cross-session)
  3. Entity Memory: knowledge graph (Postgres, cross-session)

Entities are extracted from conversations using the local LLM,
stored in Postgres with relationships, and queried by name or type.
"""
from __future__ import annotations

import asyncio
import json
import logging
from typing import Any

from sqlalchemy import select, update, func, or_
from sqlalchemy.dialects.postgresql import insert as pg_insert

from agentic_hub.models.database import get_session_factory

logger = logging.getLogger(__name__)

EXTRACT_PROMPT = """Extract named entities from this text. Return ONLY a JSON array.

Each entity should have:
- "name": entity name (proper case)
- "type": one of: project, person, stock, tool, concept, account, company, file, model
- "description": one-sentence description (optional)
- "relations": list of {"target": "entity_name", "type": "uses|contains|depends_on|trades|manages|extends"}

Example output:
[{"name": "spider.Web", "type": "project", "description": "Multi-agent AI platform", "relations": [{"target": "FastAPI", "type": "uses"}]}]

If no entities found, return: []

Text to extract from:
{text}"""


class EntityMemory:
    """Extract, store, and query entities from conversations."""

    async def extract_entities(self, text: str) -> list[dict]:
        """Use local LLM to extract entities from text.

        Runs as a background task — non-blocking to the user.
        """
        if len(text) < 20:
            return []

        prompt = EXTRACT_PROMPT.format(text=text[:3000])

        try:
            from agentic_hub.core.ollama_client import get_ollama
            from agentic_hub.core.gpu_scheduler import get_gpu_scheduler
            from agentic_hub.config import get_settings

            settings = get_settings()
            model = "qwen-fast"
            scheduler = get_gpu_scheduler()
            await scheduler.ensure_model(model)

            ollama = get_ollama()
            result = await ollama.chat_completion(
                model=model,
                messages=[
                    {"role": "system", "content": "You extract entities from text. Return ONLY valid JSON arrays."},
                    {"role": "user", "content": prompt},
                ],
                keep_alive=settings.model_keep_alive,
            )

            if not result or not result.text:
                return []

            # Parse JSON from response
            text_out = result.text.strip()
            if "```json" in text_out:
                text_out = text_out.split("```json")[1].split("```")[0].strip()
            elif "```" in text_out:
                text_out = text_out.split("```")[1].split("```")[0].strip()

            # Find JSON array in response
            start = text_out.find("[")
            end = text_out.rfind("]")
            if start >= 0 and end > start:
                text_out = text_out[start:end + 1]

            entities = json.loads(text_out)
            if not isinstance(entities, list):
                return []

            return entities

        except Exception as e:
            logger.debug(f"Entity extraction failed (non-fatal): {e}")
            return []

    async def store_entities(
        self, entities: list[dict], conversation_id: str = ""
    ) -> int:
        """Store extracted entities in Postgres. Returns count stored."""
        if not entities:
            return 0

        from agentic_hub.models.entities import Entity, EntityRelation, EntityMention

        factory = get_session_factory()
        stored = 0

        async with factory() as session:
            for ent in entities:
                name = ent.get("name", "").strip()
                etype = ent.get("type", "concept").strip().lower()
                desc = ent.get("description", "")

                if not name or len(name) < 2:
                    continue

                # Upsert entity
                stmt = pg_insert(Entity).values(
                    name=name, entity_type=etype, description=desc,
                ).on_conflict_do_update(
                    constraint="uq_entity_name_type",
                    set_={
                        "mention_count": Entity.mention_count + 1,
                        "last_seen": func.now(),
                        "description": func.coalesce(
                            # Keep existing description if new one is empty
                            desc if desc else Entity.description,
                            Entity.description,
                        ),
                    },
                )
                await session.execute(stmt)

                # Get entity ID
                result = await session.execute(
                    select(Entity.id).where(Entity.name == name, Entity.entity_type == etype)
                )
                entity_id = result.scalar_one_or_none()
                if entity_id is None:
                    continue

                # Store mention
                session.add(EntityMention(
                    entity_id=entity_id,
                    conversation_id=conversation_id,
                    context_snippet=ent.get("description", "")[:500],
                ))

                # Store relationships
                for rel in ent.get("relations", []):
                    target_name = rel.get("target", "").strip()
                    rel_type = rel.get("type", "related_to").strip()
                    if not target_name:
                        continue

                    # Ensure target entity exists
                    target_stmt = pg_insert(Entity).values(
                        name=target_name, entity_type="concept", description="",
                    ).on_conflict_do_update(
                        constraint="uq_entity_name_type",
                        set_={"mention_count": Entity.mention_count + 1},
                    )
                    await session.execute(target_stmt)

                    target_result = await session.execute(
                        select(Entity.id).where(Entity.name == target_name)
                    )
                    target_id = target_result.scalar_one_or_none()
                    if target_id:
                        rel_stmt = pg_insert(EntityRelation).values(
                            source_id=entity_id, target_id=target_id, relation_type=rel_type,
                        ).on_conflict_do_nothing(constraint="uq_entity_relation")
                        await session.execute(rel_stmt)

                stored += 1

            await session.commit()

        logger.info(f"Stored {stored} entities from conversation {conversation_id[:8] if conversation_id else 'N/A'}")
        return stored

    async def query_entity(self, name: str) -> dict | None:
        """Look up everything known about an entity by name."""
        from agentic_hub.models.entities import Entity, EntityRelation, EntityMention

        factory = get_session_factory()
        async with factory() as session:
            result = await session.execute(
                select(Entity).where(func.lower(Entity.name) == name.lower())
            )
            entity = result.scalar_one_or_none()
            if entity is None:
                return None

            # Get relations (outgoing)
            rels_out = await session.execute(
                select(EntityRelation, Entity.name.label("target_name"))
                .join(Entity, Entity.id == EntityRelation.target_id)
                .where(EntityRelation.source_id == entity.id)
            )
            relations = [
                {"target": row.target_name, "type": row.EntityRelation.relation_type}
                for row in rels_out
            ]

            # Get relations (incoming)
            rels_in = await session.execute(
                select(EntityRelation, Entity.name.label("source_name"))
                .join(Entity, Entity.id == EntityRelation.source_id)
                .where(EntityRelation.target_id == entity.id)
            )
            for row in rels_in:
                relations.append({"source": row.source_name, "type": row.EntityRelation.relation_type})

            # Get recent mentions
            mentions = await session.execute(
                select(EntityMention.context_snippet, EntityMention.conversation_id)
                .where(EntityMention.entity_id == entity.id)
                .order_by(EntityMention.created_at.desc())
                .limit(5)
            )

            return {
                "name": entity.name,
                "type": entity.entity_type,
                "description": entity.description,
                "mention_count": entity.mention_count,
                "first_seen": str(entity.first_seen),
                "last_seen": str(entity.last_seen),
                "relations": relations,
                "recent_mentions": [
                    {"snippet": m.context_snippet, "conversation": m.conversation_id}
                    for m in mentions
                ],
            }

    async def get_related_entities(self, name: str, depth: int = 2) -> list[dict]:
        """Graph traversal — find entities related to the given entity."""
        from agentic_hub.models.entities import Entity, EntityRelation

        factory = get_session_factory()
        visited: set[str] = set()
        results: list[dict] = []

        async with factory() as session:
            queue = [name.lower()]
            for d in range(depth):
                next_queue = []
                for entity_name in queue:
                    if entity_name in visited:
                        continue
                    visited.add(entity_name)

                    # Find entity
                    ent_result = await session.execute(
                        select(Entity).where(func.lower(Entity.name) == entity_name)
                    )
                    entity = ent_result.scalar_one_or_none()
                    if entity is None:
                        continue

                    if d > 0:  # Don't include the root entity
                        results.append({
                            "name": entity.name,
                            "type": entity.entity_type,
                            "description": entity.description,
                            "depth": d,
                        })

                    # Get connected entities
                    connected = await session.execute(
                        select(Entity.name)
                        .join(EntityRelation, or_(
                            EntityRelation.target_id == Entity.id,
                            EntityRelation.source_id == Entity.id,
                        ))
                        .where(or_(
                            EntityRelation.source_id == entity.id,
                            EntityRelation.target_id == entity.id,
                        ))
                        .where(Entity.id != entity.id)
                    )
                    for row in connected:
                        if row.name.lower() not in visited:
                            next_queue.append(row.name.lower())

                queue = next_queue

        return results

    async def build_entity_context(
        self, user_message: str, max_chars: int = 2000
    ) -> str:
        """Build context string from entities mentioned in or related to the message.

        Injected into agent prompts alongside RAG context.
        """
        from agentic_hub.models.entities import Entity

        # Simple keyword matching — find entities whose names appear in the message
        factory = get_session_factory()
        async with factory() as session:
            all_entities = await session.execute(
                select(Entity).order_by(Entity.mention_count.desc()).limit(100)
            )
            entities = all_entities.scalars().all()

        msg_lower = user_message.lower()
        relevant = []
        for ent in entities:
            if ent.name.lower() in msg_lower or any(
                word in msg_lower for word in ent.name.lower().split() if len(word) > 3
            ):
                relevant.append(ent)

        if not relevant:
            return ""

        lines = ["## Entity Memory (cross-session knowledge)"]
        char_count = 0
        for ent in relevant[:10]:  # Cap at 10 entities
            line = f"- **{ent.name}** ({ent.entity_type}): {ent.description or 'No description'}"
            char_count += len(line)
            if char_count > max_chars:
                break
            lines.append(line)

        return "\n".join(lines)

    async def extract_and_store_background(
        self, text: str, conversation_id: str = ""
    ) -> None:
        """Extract entities and store them. Runs as a background task."""
        entities = await self.extract_entities(text)
        if entities:
            await self.store_entities(entities, conversation_id)


# Singleton
_memory: EntityMemory | None = None


def get_entity_memory() -> EntityMemory:
    global _memory
    if _memory is None:
        _memory = EntityMemory()
    return _memory
