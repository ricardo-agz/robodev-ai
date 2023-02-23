import Head from "next/head"
import Script from "next/script"

export default function CustomHead() {
  return (
    <>
      <Head>
        <title>Neutrino AI</title>
        <meta content="width=device-width, initial-scale=1" name="viewport" />
        <meta name="neutrio AI" content="generate backend apps with only a text description" />
        <link rel="icon" href="/neutrino.png" />
        <Script type="text/javascript">
          {`
            (function(c,l,a,r,i,t,y){
                c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
                t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
                y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
            })(window, document, "clarity", "script", "fygheevc1g");
          `}
        </Script>
      </Head>
    </>
  )
}
