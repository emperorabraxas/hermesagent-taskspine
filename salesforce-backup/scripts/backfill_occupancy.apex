// Maps Lead.Property_Use__c raw codes → Opportunity.Occupancy__c picklist values.
// Property_Use__c codes are internal codes from the mortgage application plugin.
Map<String, String> codeMap = new Map<String, String>{
    'primary'   => 'Primary',
    'lab'       => 'Primary',    // mortgage plugin code for primary/owner-occupied
    'secondary' => 'Secondary',
    'vacation'  => 'Secondary',
    'rental'    => 'Investment',
    'invest'    => 'Investment',
    'workq'     => null          // unknown — skip
};

List<Lead> leads = [
    SELECT Id, Property_Use__c, ConvertedOpportunityId
    FROM Lead
    WHERE IsConverted = true
      AND ConvertedOpportunityId != null
      AND Property_Use__c != null
];

List<Id> oppIds = new List<Id>();
for (Lead l : leads) oppIds.add(l.ConvertedOpportunityId);

Map<Id, Opportunity> opps = new Map<Id, Opportunity>([
    SELECT Id, Occupancy__c FROM Opportunity
    WHERE Id IN :oppIds AND Occupancy__c = null
]);

List<Opportunity> toUpdate = new List<Opportunity>();
Integer skipped = 0;
for (Lead l : leads) {
    if (!opps.containsKey(l.ConvertedOpportunityId)) continue;
    String mapped = codeMap.get(l.Property_Use__c.toLowerCase());
    if (mapped == null) { skipped++; continue; }
    toUpdate.add(new Opportunity(Id = l.ConvertedOpportunityId, Occupancy__c = mapped));
}

if (!toUpdate.isEmpty()) { update toUpdate; }
System.debug('Backfilled: ' + toUpdate.size() + ' | Skipped (unknown code): ' + skipped);
