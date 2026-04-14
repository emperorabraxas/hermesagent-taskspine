/**
 * OpportunityTriggerHandler
 *
 * Automated stage advancement for the Nexa Loan Pipeline.
 * Stages only advance forward, never backward.
 */
public with sharing class OpportunityTriggerHandler {

    private static final List<String> STAGE_ORDER = new List<String>{
        'File Import',      // 0
        'Credit Pulled',    // 1
        'Doc Signed',       // 2
        'Submitted',        // 3
        'AWC',              // 4
        'STP',              // 5
        'CTC',              // 6
        'Title CTC',        // 7
        'Closing',          // 8
        'Funded'            // 9
    };

    // Cache field existence so we don't describe on every record
    private static Map<String, Boolean> fieldExists;
    static {
        fieldExists = new Map<String, Boolean>();
        Map<String, Schema.SObjectField> fm = Opportunity.SObjectType.getDescribe(SObjectDescribeOptions.DEFERRED).fields.getMap();
        for (String f : new List<String>{
            'credit_pulled__c','docs_signed__c','title_ctc__c',
            'uwm_1003_signature_date__c','uwm_status__c',
            'uwm_clear_to_close_date__c','uwm_disbursement_date__c',
            'closer__c','processor__c'
        }) {
            fieldExists.put(f, fm.containsKey(f));
        }
    }

    public static void handleBeforeUpsert(List<Opportunity> newList, Map<Id, Opportunity> oldMap) {
        syncSalesDirectorFromLoanOfficer(newList, oldMap);
    }

    public static void handleAfterUpdate(List<Opportunity> newList, Map<Id, Opportunity> oldMap) {
        List<Opportunity> toUpdate = new List<Opportunity>();

        for (Opportunity opp : newList) {
            Opportunity old = oldMap.get(opp.Id);
            String targetStage = evaluateStageAdvancement(opp, old);

            if (targetStage != null && targetStage != opp.StageName) {
                Integer currentIdx = stageIndex(opp.StageName);
                Integer targetIdx  = stageIndex(targetStage);
                if (targetIdx > currentIdx) {
                    toUpdate.add(new Opportunity(Id = opp.Id, StageName = targetStage));
                }
            }
        }

        if (!toUpdate.isEmpty()) {
            update toUpdate;
        }
    }

    private static void syncSalesDirectorFromLoanOfficer(List<Opportunity> newList, Map<Id, Opportunity> oldMap) {
        Set<Id> loIds = new Set<Id>();

        for (Opportunity opp : newList) {
            Opportunity oldOpp = oldMap == null ? null : oldMap.get(opp.Id);
            Boolean loChanged = oldOpp == null || opp.LO__c != oldOpp.LO__c;
            Boolean needsBackfill = opp.LO__c != null && opp.Sales_Director__c == null;

            if ((loChanged || needsBackfill) && opp.LO__c != null) {
                loIds.add(opp.LO__c);
            }
        }

        if (loIds.isEmpty()) {
            for (Opportunity opp : newList) {
                Opportunity oldOpp = oldMap == null ? null : oldMap.get(opp.Id);
                if (oldOpp != null && oldOpp.LO__c != null && opp.LO__c == null) {
                    opp.Sales_Director__c = null;
                }
            }
            return;
        }

        Map<Id, User> loanOfficers = new Map<Id, User>([
            SELECT Id, ManagerId
            FROM User
            WHERE Id IN :loIds
        ]);

        for (Opportunity opp : newList) {
            Opportunity oldOpp = oldMap == null ? null : oldMap.get(opp.Id);
            Boolean loChanged = oldOpp == null || opp.LO__c != oldOpp.LO__c;
            Boolean needsBackfill = opp.LO__c != null && opp.Sales_Director__c == null;

            if (opp.LO__c == null) {
                if (oldOpp != null && oldOpp.LO__c != null) {
                    opp.Sales_Director__c = null;
                }
                continue;
            }

            if (!loChanged && !needsBackfill) {
                continue;
            }

            User loanOfficer = loanOfficers.get(opp.LO__c);
            opp.Sales_Director__c = loanOfficer == null ? null : loanOfficer.ManagerId;
        }
    }

    private static String evaluateStageAdvancement(Opportunity opp, Opportunity old) {
        // ── Funded (9)
        if (statusChangedTo(opp, old, new Set<String>{'closed', 'funded'})) return 'Funded';
        if (changedToNonNull(opp, old, 'uwm_disbursement_date__c')) return 'Funded';

        // ── Closing (8)
        if (changedToNonNull(opp, old, 'closer__c')) return 'Closing';

        // ── Title CTC (7)
        if (checkboxFlipped(opp, old, 'title_ctc__c')) return 'Title CTC';

        // ── CTC (6)
        if (statusChangedTo(opp, old, new Set<String>{'clear to close', 'ctc'})) return 'CTC';
        if (changedToNonNull(opp, old, 'uwm_clear_to_close_date__c')) return 'CTC';

        // ── STP (5)
        if (changedToNonNull(opp, old, 'processor__c')) return 'STP';

        // ── AWC (4)
        if (statusChangedTo(opp, old, new Set<String>{'approved', 'awc', 'approved with conditions'})) return 'AWC';

        // ── Submitted (3): button-driven, not trigger-driven

        // ── Doc Signed (2)
        if (changedToNonNull(opp, old, 'uwm_1003_signature_date__c')) return 'Doc Signed';
        if (checkboxFlipped(opp, old, 'docs_signed__c')) return 'Doc Signed';

        // ── Credit Pulled (1)
        if (checkboxFlipped(opp, old, 'credit_pulled__c')) return 'Credit Pulled';

        return null;
    }

    private static Boolean statusChangedTo(Opportunity opp, Opportunity old, Set<String> targets) {
        if (!fieldExists.get('uwm_status__c')) return false;
        String newStatus = safeString(opp, 'UWM_Status__c');
        String oldStatus = safeString(old, 'UWM_Status__c');
        if (String.isBlank(newStatus)) return false;
        String lower = newStatus.toLowerCase();
        for (String t : targets) {
            if (lower.contains(t)) {
                // Only fire if the OLD status didn't already match
                if (String.isNotBlank(oldStatus) && oldStatus.toLowerCase().contains(t)) return false;
                return true;
            }
        }
        return false;
    }

    private static Boolean changedToNonNull(Opportunity opp, Opportunity old, String fieldKey) {
        if (!fieldExists.containsKey(fieldKey) || !fieldExists.get(fieldKey)) return false;
        String apiName = fieldKey.endsWith('__c') ? fieldKey : fieldKey + '__c';
        // Use the casing from the field map
        Object newVal = opp.get(apiName);
        Object oldVal = old.get(apiName);
        return newVal != null && oldVal == null;
    }

    private static Boolean checkboxFlipped(Opportunity opp, Opportunity old, String fieldKey) {
        if (!fieldExists.containsKey(fieldKey) || !fieldExists.get(fieldKey)) return false;
        Object newVal = opp.get(fieldKey);
        Object oldVal = old.get(fieldKey);
        return newVal == true && oldVal != true;
    }

    private static String safeString(Opportunity opp, String fieldName) {
        try {
            return (String) opp.get(fieldName);
        } catch (Exception e) {
            return null;
        }
    }

    private static Integer stageIndex(String stageName) {
        for (Integer i = 0; i < STAGE_ORDER.size(); i++) {
            if (STAGE_ORDER[i] == stageName) return i;
        }
        return -1;
    }
}
