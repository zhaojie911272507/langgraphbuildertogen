import type { NextPage } from 'next'
import Head from 'next/head'

import Page from '@/components'

const Home: NextPage = () => {
  return (
    <div>
      <Head>
        <title>LangGraph Builder</title>
        <meta name='description' content='LangGraph Builder' />
        <link rel='icon' href='/favicon.ico' />
      </Head>
      <Page />
    </div>
  )
}

export default Home
