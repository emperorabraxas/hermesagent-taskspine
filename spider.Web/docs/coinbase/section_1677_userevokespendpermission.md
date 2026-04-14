# useRevokeSpendPermission
Source: https://docs.cdp.coinbase.com/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Functions/useRevokeSpendPermission



```ts theme={null}
function useRevokeSpendPermission(): UseRevokeSpendPermissionReturnType;
```

Hook that provides a wrapped function to revoke spend permissions for EVM Smart Accounts with enhanced developer experience.
This hook automatically handles user operation tracking and provides status updates.

## Returns

[`UseRevokeSpendPermissionReturnType`](/sdks/cdp-sdks-v2/frontend/@coinbase/cdp-hooks/Type-Aliases/UseRevokeSpendPermissionReturnType)

## Example

```tsx lines theme={null}
function RevokeSpendPermission({ permissionHash }) {
  const { revokeSpendPermission, data, error, status } = useRevokeSpendPermission();

  const handleRevokeSpendPermission = async () => {
    try {
      const result = await revokeSpendPermission({
        network: "base-sepolia",
        permissionHash: permissionHash,
        useCdpPaymaster: true
      });
      console.log("User Operation Hash:", result.userOperationHash);
    } catch (error) {
      console.error("Failed to revoke spend permission:", error);
    }
  };

  return (
    <div>
      {status === "pending" && <p>Revoking permission...</p>}
      {status === "success" && data && (
        <div>
          <p>Permission revoked successfully!</p>
          <p>Transaction Hash: {data.transactionHash}</p>
        </div>
      )}
      {status === "error" && <p>Error: {error?.message}</p>}
      <button onClick={handleRevokeSpendPermission}>
        Revoke Permission
      </button>
    </div>
  );
}
```

