import { LightningElement, api, wire } from 'lwc';
import { getRecord, updateRecord } from 'lightning/uiRecordApi';
import { ShowToastEvent } from 'lightning/platformShowToastEvent';
import STAGE_FIELD from '@salesforce/schema/Opportunity.StageName';

const FIELDS = ['Opportunity.StageName'];

const STAGE_ORDER = [
    'File Import', 'Credit Pulled', 'Doc Signed', 'Submitted',
    'AWC', 'STP', 'CTC', 'Title CTC', 'Closing', 'Funded'
];

export default class SubmitToUwmButton extends LightningElement {
    @api recordId;

    stageName = '';
    submitting = false;

    @wire(getRecord, { recordId: '$recordId', fields: FIELDS })
    wiredOpp({ data }) {
        if (data) {
            this.stageName = data.fields.StageName.value || '';
        }
    }

    get stageIndex() {
        return STAGE_ORDER.indexOf(this.stageName);
    }

    get docSignedIndex() {
        return STAGE_ORDER.indexOf('Doc Signed');
    }

    get submittedIndex() {
        return STAGE_ORDER.indexOf('Submitted');
    }

    get isReady() {
        // Only enabled when at Doc Signed — not before, not after
        return this.stageIndex === this.docSignedIndex;
    }

    get isDisabled() {
        return !this.isReady || this.submitting;
    }

    get buttonLabel() {
        if (this.stageIndex >= this.submittedIndex) return 'Submitted';
        return this.submitting ? 'Submitting...' : 'Submit Loan';
    }

    get buttonVariant() {
        return this.isReady ? 'brand' : 'neutral';
    }

    async handleClick() {
        if (this.isDisabled) return;
        this.submitting = true;
        try {
            await updateRecord({
                fields: {
                    Id: this.recordId,
                    [STAGE_FIELD.fieldApiName]: 'Submitted'
                }
            });
            this.stageName = 'Submitted';
            this.dispatchEvent(new ShowToastEvent({
                title: 'Submitted',
                message: 'Loan submitted to UWM.',
                variant: 'success'
            }));
        } catch (e) {
            this.dispatchEvent(new ShowToastEvent({
                title: 'Error',
                message: e?.body?.message || 'Failed to submit.',
                variant: 'error'
            }));
        } finally {
            this.submitting = false;
        }
    }
}
