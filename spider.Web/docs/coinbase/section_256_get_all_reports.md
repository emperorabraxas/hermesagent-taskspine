# Get all reports
Source: https://docs.cdp.coinbase.com/api-reference/exchange-api/rest-api/reports/get-all-reports

GET /reports
Gets a list of all user generated reports.

<Info>
  Once a report request has been accepted for processing, you can poll the report resource endpoint at `/reports/{report_id}` for its status. When status is `ready`, the final report is uploaded and available at `{file_url}`.
</Info>

## API Key Permissions

This endpoint requires either the "view" or "trade" permission.

