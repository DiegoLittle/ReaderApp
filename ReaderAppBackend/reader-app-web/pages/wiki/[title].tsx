import React, { useEffect, useState } from 'react'
import { PlusIcon } from '@heroicons/react/solid'
import { useRouter } from 'next/router'
import {
  CodeIcon,
  BookOpenIcon,
  DatabaseIcon
} from '@heroicons/react/solid'
import DatasetCard from '../../components/dataset_card'
import DatasetTemplate from '../../page_templates/dataset_wiki'
import DefaultTemplate from '../../page_templates/default'
import TaskTemplate from '../../page_templates/task_template'

const WikiPage = ({ title }) => {
  const [page, setPage] = useState(null)
  const router = useRouter()
  const [data, setData] = useState(null)
  const [error, setError] = useState(false)
  const [loading, setLoading] = useState(true)

  async function fetch_page() {
    // Should probably be slug instead of title
    // multiple slugs can exist for the same page title
    console.log(title)
    console.log("Fetching page for " + title)
    let res = await fetch('/api/wiki?title=' + title)
    let data = await res.json()
    if (data.wikipedia_link){
      router.push(data.wikipedia_link)
    }
    console.log(data)

    console.log(data)
    setData(data)
    if (data.error) {
      setError(true)
    }
    else {
      setError(false)
    }
    setLoading(false)

  }
  useEffect(() => {
    setLoading(true)
    console.log("Fetching page for " + title)
    fetch_page()
  }, [title])
  function renderSwitch() {
    // console.log("Data type: "+ data.type)
    switch(data.type) {
      case 'dataset':
        return <DatasetTemplate data={data}></DatasetTemplate>;
      case 'task':
        return <TaskTemplate data={data}></TaskTemplate>;
      default:
        return <DefaultTemplate data={data}></DefaultTemplate>;
    }
  }

  return (
    <div>
      {!loading ?
        <>
          {error ?
            <div className="text-center mt-16">

              <h3 className="mt-2 font-medium text-gray-900 text-lg">{data.message}</h3>
              <p className="mt-1 text-gray-500">You might be looking for ...</p>
              <p>{data.suggestions && data.suggestions.labels.map((suggestion) =>
                  <div
                    className=' w-72 mx-auto text-left my-2 bg-blue-50 rounded-lg cursor-pointer p-1 '
                    onClick={() => {

                      router.push("/wiki/" + suggestion['name'])
                    }}>
                    <div className='text-lg'>
                      {suggestion['name']}
                    </div>
                        <div className='bg-blue-100 p-0.5 rounded-lg inline-flex'>
                          {suggestion['type']}
                        </div>
                    </div>
              )}</p>
                </div>
            : 
            <>
            {
              renderSwitch()
            }
            </>
          }
          </>
              :
              <div className="h-screen flex justify-center mt-40">
                <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-200"></div>
              </div>
      }
            </div>
  )
}

          export default WikiPage
          import N3 from 'n3'
          import {fetch_dataset} from '../../lib/mongo_methods'
          import {MongoClient} from 'mongodb';
          import Link from 'next/link'
// import {SparqlEndpointFetcher} from "fetch-sparql-endpoint";
          const SparqlClient = require('sparql-http-client')



          export async function getServerSideProps(context) {
            let {title} = context.query
          console.log(title)
          return {
            props: {
            title: title
    }
  }
}

// const myFetcher = new SparqlEndpointFetcher();
// import {MongoClient} from 'mongodb'
// export async function getServerSideProps(context) {
            //   const { title,type } = context.query;
            //   var redirect = false;
            //   var data = {
            //     title: title,
            //   }

            //   let res = await fetch("http://localhost:8000/api/wiki/?q="+title)
            //   let json = await res.json()
            //   data = json
            //   if(data){
            //     redirect = data.wikipedia_link
            //   }


            //   if(type == "dataset"){
            //     let dataset = await fetch_dataset(title)
            //     console.log(dataset)
            //     // redirect = "https://paperswithcode.com/dataset/" + title.replace(" ", "-")
            //   }
            //   if(redirect){
            //   return {
            //     redirect: {
            //       destination: redirect,
            //       permanent: false,
            //     },
            //   }
            // }
            // else{
            //   return {
            //     props: {
            //       data:data
            //     }
            //   }
            // }

            // }

            // https://paperswithcode.com/dataset/mit-indoors-scenes


            async function fetch_same_as() {
              // console.log(title)
              // console.log(type)
              // var redirect = null
              // const myFetcher = new SparqlEndpointFetcher({
              //   method: 'POST',                           // A custom HTTP method for issuing (non-update) queries, defaults to POST. Update queries are always issued via POST.
              //   additionalUrlParams: new URLSearchParams({'infer': 'true', 'sameAs': 'false'});  // A set of additional parameters that well be added to fetchAsk, fetchBindings & fetchTriples requests
              //   fetch: fetch,                             // A custom fetch-API-supporting function
              //   dataFactory: DataFactory,                 // A custom RDFJS data factory
              //   prefixVariableQuestionMark: false         // If variable names in bindings should be prefixed with '?', defaults to false
              // });

              const endpointUrl = 'https://scholkg.kmi.open.ac.uk/sparqlendpoint'
              const query = `
PREFIX http: <http://www.w3.org/2011/http#>
PREFIX sd: <http://www.w3.org/ns/sparql-service-description#>
PREFIX cs: <http://purl.org/vocab/changeset/schema#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX pr: <http://purl.org/ontology/prv/core#>
# Example query: Select all statements about Wikipedia.  
PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
PREFIX cskg: <http://scholkg.kmi.open.ac.uk/cskg/resource/> # CS-KG resources 
PREFIX cskg-ont: <http://scholkg.kmi.open.ac.uk/cskg/ontology#> # CS-KG ontology 
PREFIX provo: <http://www.w3.org/ns/prov#> 
PREFIX cso: <http://cso.kmi.open.ac.uk/schema/cso#> 
PREFIX owl: <http://www.w3.org/2002/07/owl#>
 
SELECT ?sub ?type_sub ?pre ?obj ?type_obj ?sup FROM <http://scholkg.kmi.open.ac.uk/cskg> 
WHERE {
{ 
  cskg:neural_network ?pre ?obj 
  FILTER(isUri(?pre) && STRSTARTS(STR(?pre), STR(owl:)))
  } 

}
  ORDER BY DESC (?sup) LIMIT 500
`

              // const client = new SparqlClient({ endpointUrl: 'https://query.wikidata.org/sparql' })
              // const stream = await client.query.select(`
              //   PREFIX wdt: <http://www.wikidata.org/prop/direct/>
              //   PREFIX wd: <http://www.wikidata.org/entity/>
              //   PREFIX schema: <http://schema.org/>
              //   PREFIX wikibase: <https://wikiba.se/ontology>

              //   SELECT ?o WHERE {
              //     wd:Q192776 schema:description ?o .
              //     FILTER((LANG(?o)) = "en")

              //   }
              // `)


              const client = new SparqlClient({ endpointUrl })
              const stream = await client.query.select(query)

              await stream.on('data', row => {
                // console.log(row)
                Object.entries(row).forEach(([key, value]) => {
                  console.log(key, value.value)
                  var definition = value.value
                  data.definition = definition
                  // console.log(`${key}: ${value.value} (${value.termType})`)
                })
              })

              var end = new Promise(function (resolve, reject) {
                stream.on('end', () => resolve(stream));
                stream.on('error', reject); // or something like that. might need to close `hash`
              });
              await end

            }

async function cso_link(title) {

            let res = await fetch(`https://cso.kmi.open.ac.uk/topics/${title.replace(" ", "_")}.ttl`)
          let data = await res.text()
          let parser = new N3.Parser()
          var store = new N3.Store();
  const myPromise = new Promise((resolve, reject) => {
            parser.parse(data, (err, triple, prefixes) => {
              // Create a new promise
              if (err) {
                console.log(err)
              }
              else {
                // console.log(typeof(triples))
                if (triple) {
                  // console.log(triple)
                  store.addQuad(triple)
                }
                else {
                  resolve(store)
                }

              }
            })
          });
          let await_parse = await myPromise
          for (let index = 0; index < store.getQuads(null, "http://schema.org/relatedLink", null, null).length; index++) {
    const quad = store.getQuads(null, "http://schema.org/relatedLink", null, null)[index];
          if (quad.object.value.startsWith('http://en.wikipedia.org/wiki/')) {
            console.log("found wikipedia link")
      redirect = quad.object.value
          break
    }
  }
}