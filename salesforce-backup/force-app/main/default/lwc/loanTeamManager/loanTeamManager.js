import { LightningElement, api, wire } from 'lwc';
import { getRecord } from 'lightning/uiRecordApi';
import { ShowToastEvent } from 'lightning/platformShowToastEvent';
import { refreshApex } from '@salesforce/apex';

const TEAM_FIELDS = [
    'OwnerId', 'Owner.Name',
    'Junior_LO__c', 'Junior_LO__r.Name',
    'LOA__c', 'LOA__r.Name',
    'LO__c', 'LO__r.Name',
    'Processor__c', 'Processor__r.Name',
    'Closer__c', 'Closer__r.Name',
    'Sales_Director__c', 'Sales_Director__r.Name',
    'Pipeline_Director__c', 'Pipeline_Director__r.Name'
];

const LEAD_FIELDS = TEAM_FIELDS.map(f => `Lead.${f}`);
const OPP_FIELDS = TEAM_FIELDS.map(f => `Opportunity.${f}`);

export default class LoanTeamManager extends LightningElement {
    @api recordId;
    @api objectApiName;

    _wiredResult;
    teamMembers = [];
    isEditing = null;

    get isLead() { return this.objectApiName === 'Lead'; }
    get wireFields() { return this.isLead ? LEAD_FIELDS : OPP_FIELDS; }

    @wire(getRecord, { recordId: '$recordId', optionalFields: '$wireFields' })
    wiredRecord(result) {
        this._wiredResult = result;
        if (result.data) {
            this.teamMembers = this._buildTeam(result.data);
        } else if (result.error) {
            this.teamMembers = [];
        }
    }

    get hasTeam() { return this.teamMembers.length > 0; }

    get enrichedTeam() {
        return this.teamMembers.map(m => ({
            ...m,
            isEditingThis: this.isEditing === m.key,
            isRequired: !this.isLead && m.key === 'salesDirector',
            nameClass: m.assigned ? 'team-name' : 'team-name-unassigned'
        }));
    }

    _val(data, fieldName) {
        return data.fields?.[fieldName]?.value || null;
    }

    _name(data, relName) {
        return data.fields?.[relName]?.value?.fields?.Name?.value || 'Unassigned';
    }

    _buildTeam(data) {
        // Roles match the custom profiles built for the org
        const roles = [
            { key: 'jloa',             role: 'Jr LOA',             field: 'Junior_LO__c',        rel: 'Junior_LO__r' },
            { key: 'loa',              role: 'LOA',                field: 'LOA__c',              rel: 'LOA__r' },
            { key: 'lo',               role: 'LO',                field: 'LO__c',               rel: 'LO__r' },
            { key: 'salesDirector',    role: 'Sales Director',     field: 'Sales_Director__c',   rel: 'Sales_Director__r' },
            { key: 'pipelineDirector', role: 'Pipeline Director',  field: 'Pipeline_Director__c',rel: 'Pipeline_Director__r' },
            { key: 'processor',        role: 'Processor',          field: 'Processor__c',        rel: 'Processor__r' },
            { key: 'closer',           role: 'Closer',             field: 'Closer__c',           rel: 'Closer__r' }
        ];

        return roles
            .filter(r => data.fields?.hasOwnProperty(r.field))
            .map(r => ({
                key: r.key,
                role: r.role,
                userId: this._val(data, r.field),
                userName: this._name(data, r.rel),
                fieldApiName: r.field,
                assigned: !!this._val(data, r.field),
                icon: 'standard:user'
            }));
    }

    handleEdit(event) {
        event.preventDefault();
        const role = event.currentTarget.dataset.role;
        // Toggle: clicking Change on the same role closes it
        this.isEditing = this.isEditing === role ? null : role;
    }

    handleFieldChange(event) {
        const role = event.target?.dataset?.role;
        if (!role) return;
        const form = event.target.closest('lightning-record-edit-form');
        if (form) form.submit();
    }

    handleSaveSuccess() {
        this.isEditing = null;
        refreshApex(this._wiredResult);
        this.dispatchEvent(new ShowToastEvent({
            title: 'Team Updated',
            message: 'Assignment saved.',
            variant: 'success'
        }));
    }

    handleSaveError(event) {
        const msg = event?.detail?.message || 'Failed to update team member.';
        this.dispatchEvent(new ShowToastEvent({
            title: 'Error',
            message: msg,
            variant: 'error'
        }));
    }
}
