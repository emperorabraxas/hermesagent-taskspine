/**
 * LeadTriggerHandler
 *
 * Keeps Sales Director aligned with the selected LO's User.Manager.
 */
public with sharing class LeadTriggerHandler {

    public static void handleBeforeUpsert(List<Lead> newList, Map<Id, Lead> oldMap) {
        Set<Id> loIds = new Set<Id>();

        for (Lead leadRecord : newList) {
            Lead oldLead = oldMap == null ? null : oldMap.get(leadRecord.Id);
            Boolean loChanged = oldLead == null || leadRecord.LO__c != oldLead.LO__c;
            Boolean needsBackfill = leadRecord.LO__c != null && leadRecord.Sales_Director__c == null;

            if ((loChanged || needsBackfill) && leadRecord.LO__c != null) {
                loIds.add(leadRecord.LO__c);
            }
        }

        Map<Id, User> loanOfficers = loIds.isEmpty()
            ? new Map<Id, User>()
            : new Map<Id, User>([
                SELECT Id, ManagerId
                FROM User
                WHERE Id IN :loIds
            ]);

        for (Lead leadRecord : newList) {
            Lead oldLead = oldMap == null ? null : oldMap.get(leadRecord.Id);
            Boolean loChanged = oldLead == null || leadRecord.LO__c != oldLead.LO__c;
            Boolean needsBackfill = leadRecord.LO__c != null && leadRecord.Sales_Director__c == null;

            if (leadRecord.LO__c == null) {
                if (oldLead != null && oldLead.LO__c != null) {
                    leadRecord.Sales_Director__c = null;
                }
                continue;
            }

            if (!loChanged && !needsBackfill) {
                continue;
            }

            User loanOfficer = loanOfficers.get(leadRecord.LO__c);
            leadRecord.Sales_Director__c = loanOfficer == null ? null : loanOfficer.ManagerId;
        }
    }
}
