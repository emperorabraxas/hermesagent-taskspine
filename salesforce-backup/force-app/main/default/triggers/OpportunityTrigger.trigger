/**
 * OpportunityTrigger
 *
 * Thin trigger — all logic lives in OpportunityTriggerHandler.
 * Handles stage automation for the Nexa Loan Pipeline path.
 */
trigger OpportunityTrigger on Opportunity (before insert, before update, after update) {
    if (Trigger.isBefore) {
        OpportunityTriggerHandler.handleBeforeUpsert(Trigger.new, Trigger.oldMap);
    }

    if (Trigger.isAfter && Trigger.isUpdate) {
        OpportunityTriggerHandler.handleAfterUpdate(Trigger.new, Trigger.oldMap);
    }
}
