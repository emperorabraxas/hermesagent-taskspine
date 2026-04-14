# Partial and full staking app
Source: https://docs.cdp.coinbase.com/get-started/demo-apps/app-examples/partial-and-full-staking-app

A partial and full ETH staking app powered by our fully self-serviceable Staking API with no gated onboarding.

<LearnButtons />

<Tags />

<div>
  <Frame>
    <img />
  </Frame>
</div>

## Coinbase StakeMyETH | Backend

<div>
  <img alt="NodeJS" />

  <img alt="TypeScript" />

  <img alt="Coinbase" />
</div>

### Prerequisites

* [Node](https://nodejs.org/en/download)

### Installation

```bash lines wrap theme={null}
pnpm i
```

* Fill in the environment variables in the `.env` file, refer to the `.env.example` file for the required variables.
* Create a [CDP API key](https://portal.cdp.coinbase.com/projects/api-keys) and save it as `cdp_api_key.json` in the root of the repository, refer to [cdp\_api\_key.example.json](https://github.com/HeimLabs/coinbase-myusdc-backend/blob/main/cdp_api_key.example.json).

***

### Usage `(in development mode)`

Start the Express Server

```bash lines wrap theme={null}
pnpm run dev
```

***

### Usage `(in production mode)`

Build the project

```bash lines wrap theme={null}
pnpm run build
```

Start the Express Server

```bash lines wrap theme={null}
pnpm start
```

## Coinbase StakeMyETH | Frontend

<div>
  <img alt="React" />

  <img alt="Vite" />

  <img alt="TypeScript" />

  <img alt="SCSS" />

  <img alt="Coinbase" />

  <img alt="Pnpm" />
</div>

### Prerequisites

* Git
* NodeJs
* pnpm

### Getting Started

* Install dependencies

```sh lines wrap theme={null}
pnpm i
```

* Fill in the environment variables in the `.env` file, refer to the `.env.example` file for the required variables.

### Run Dev

```sh lines wrap theme={null}
pnpm run dev
```

### Build Prod

```sh lines wrap theme={null}
pnpm run build
```

