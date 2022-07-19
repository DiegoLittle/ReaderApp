import React, { useEffect, useState } from 'react'
import { PlusIcon } from '@heroicons/react/solid'
import { useRouter } from 'next/router'
import {
  CodeIcon,
  BookOpenIcon,
  DatabaseIcon
} from '@heroicons/react/solid'
import DatasetCard from '../components/dataset_card'
import ReactMarkdown from 'react-markdown'


const WikiPage = ({ data }) => {
  const [page, setPage] = useState(null)
  const router = useRouter()
  const [error, setError] = useState(false)
  const [loading, setLoading] = useState(true)






  return (
    <div>
      <>
        <div
          
          className='grid p-8'>


          {/* Infobox */}
          <div style={{
            gridColumn: "span 2 / span 2",
          }}>
            <h1 className='text-3xl font-semibold'>{data.title[0].toUpperCase() + data.title.substring(1)}</h1>
            <div className='flex mb-2 mt-1'>
              {data.type &&
                <div className='mr-2 bg-blue-300 rounded-lg p-1 text-sm cursor-pointer'>
                  <Link href={"/wiki/" + data.type}>
                    <span >{data.type[0].toUpperCase() + data.type.substring(1)}</span>
                  </Link>
                </div>
              }
              {data.tags && data.tags.map((tag) =>
                <Link href={"/wiki/" + tag}>
                  <span className='bg-blue-100 rounded-lg p-1 ml-1 text-sm cursor-pointer'>
                    {tag[0].toUpperCase() + tag.substring(1)}
                  </span>
                </Link>
              )}
            </div>
          </div>
          <h1 
                      style={{
                        gridColumn: "span 10 / span 10"
                      }}
          className='text-lg '><ReactMarkdown>{data.description}</ReactMarkdown></h1>
          <div className='my-8'>
            {data.related_papers &&
              <>
                <h1 className='text-xl font-semibold'>Related Papers</h1>
                <div className=''>
                  {data.related_papers.map((paper) =>
                    // <Link href={paper.paper_url}>
                    <div className='my-4 shadow-md p-2 '>

                      <div className='text-lg font-semibold'>{paper.title}</div>

                      <div>{paper.authors ?? paper.authors.map((author) =>
                        <span>{author}</span>
                      )}</div>
                      <div>{paper.date}</div>
                      <div className='flex my-2'>
                        {paper.code_url &&
                          <a target={"_blank"} href={paper.code_url}>
                            <CodeIcon className='h-6 w-6 p-0.5 bg-blue-100 rounded-xl hover:bg-blue-200 cursor-pointer mr-2'></CodeIcon>
                          </a>
                        }
                        {paper.paper_url &&
                          <a target={"_blank"} href={paper.paper_url}>
                            <BookOpenIcon className='h-6 w-6 p-0.5 bg-blue-100 rounded-xl hover:bg-blue-200 cursor-pointer mr-2'></BookOpenIcon>
                          </a>
                        }
                      </div>
                    </div>



                    // </Link>
                  )}
                </div>
              </>
            }
          </div>
          <div className='my-8'>
            {data.datasets &&
              <>
                <h1 className='text-xl font-semibold'>Datasets</h1>
                <div className=''>
                  {data.datasets && data.datasets.map((dataset) =>
                    // <Link href={paper.paper_url}>
                    <DatasetCard dataset={dataset} />
                    // </Link>
                  )}
                </div>
              </>}
          </div>
          {data.related_concepts &&
            <div className='my-8'>
              <h1 className='text-xl font-semibold'>Related Concepts</h1>
            </div>
          }
        </div>


      </>


    </div>
  )
}

export default WikiPage
import N3 from 'n3'
import { fetch_dataset } from '../../lib/mongo_methods'
import { MongoClient } from 'mongodb';
import Link from 'next/link'
// import {SparqlEndpointFetcher} from "fetch-sparql-endpoint";
const SparqlClient = require('sparql-http-client')



export async function getServerSideProps(context) {
  let { title } = context.query
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