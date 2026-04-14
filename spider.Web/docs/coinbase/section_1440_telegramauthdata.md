# TelegramAuthData
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-core/Interfaces/TelegramAuthData



Raw Telegram auth data received from the Telegram popup via postMessage.
Uses snake\_case field names matching Telegram's response format.

## Properties

| Property            | Type     | Description                                                           |
| ------------------- | -------- | --------------------------------------------------------------------- |
| <a /> `id`          | `number` | The Telegram user ID.                                                 |
| <a /> `first_name?` | `string` | The Telegram user's first name.                                       |
| <a /> `last_name?`  | `string` | The Telegram user's last name.                                        |
| <a /> `username?`   | `string` | The Telegram user's username.                                         |
| <a /> `photo_url?`  | `string` | The Telegram user's profile picture URL.                              |
| <a /> `auth_date`   | `number` | The Telegram user's last login as a Unix timestamp.                   |
| <a /> `hash`        | `string` | The hash of the Telegram user data used for verifying data integrity. |

