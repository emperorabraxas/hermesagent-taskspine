/**
 * LeadTrigger
 *
 * Keeps Sales Director aligned with the selected LO's User.Manager.
 */
trigger LeadTrigger on Lead (before insert, before update) {
    LeadTriggerHandler.handleBeforeUpsert(Trigger.new, Trigger.oldMap);
}
