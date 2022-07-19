import React from 'react'
import { useRouter } from 'next/router'
import dynamic from "next/dynamic";

const ReadHome = ({url}) => {
    const PDFViewer = dynamic(() => import("../../components/pdf-view"), {
        ssr: false
      });
  return (
    <div>
        {url? 
        
        <PDFViewer url={url}></PDFViewer>:
        <SearchBox></SearchBox>

    }
        {/* <SearchBox></SearchBox> */}
    </div>
  )
}

export default ReadHome


export async function getServerSideProps(context){
    var { url } = context.query;
    if(typeof url == 'undefined'){
        url = null
    }
    
    console.log(url)

    return {
        props:{
            url
        }
    }
}

import { useEffect, useState } from 'react'
function classNames(...classes) {
  return classes.filter(Boolean).join(' ')
}

function SearchBox({}) {
    const router = useRouter()

  const[query,setQuery] = useState(false)

  function loadPDF(){
    if(query){
        console.log(query)
        router.push((`/read?url=${query}`))
    }
  }

  return (
    <div className={"lg:mx-32"} >
      {/* <Combobox.Label className="block text-sm font-medium text-gray-700">Assigned to</Combobox.Label> */}
      <div className="relative mt-1">
        <label className='flex text-center font-semibold my-8 text-2xl justify-center'>Enter a URL</label>
        <div className="flex w-2/3 lg:w-1/2 mx-auto rounded-lg border border-gray-300 bg-white py-1 pl-1 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 sm:text-sm">
         
        
        <input
        className='w-full focus:outline-none ml-1'
        onKeyDown={(e)=>{
          if(e.key==='Enter'){
            loadPDF()
          }
        }}
        autoComplete='off'
          onChange={(event) => {
            setQuery(event.target.value)
          }
        }
        />
        </div>
        {/* <Combobox.Button className="absolute inset-y-0 right-0 flex items-center rounded-r-md px-2 focus:outline-none">
          <SelectorIcon className="h-5 w-5 text-gray-400" aria-hidden="true" />
        </Combobox.Button> */}
{/* {Object.keys(results).length>0&&
<>
        {results.methods.length > 0 && (
          <Combobox.Options className="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
            {results.methods.map((result) => (
              <Link href={`/${result.type}/${result.label}`}>
              <Combobox.Option
                // key={result.id}
                value={result.label}
                className={({ active }) =>
                  classNames(
                    'relative cursor-pointer select-none py-2 pl-3 pr-9',
                    result.type=='dataset' && 'bg-indigo-100 text-indigo-800',
                    result.type=='method' && 'bg-green-100 text-green-800',
                    result.type=='paper' && 'bg-blue-100 text-blue-800',
                    result.type=='task' && 'bg-orange-100 text-orange-800',
                    active ? 'bg-indigo-600 text-white' : 'text-gray-900'
                  )
                }
              >
                {({ active, selected }) => (
                  <>
                  <div className="flex">
                    <span className={classNames('block truncate', selected && 'font-semibold')}>{result.label}</span>
                    <span className="ml-8 bg-gray-100 p-1 rounded-lg">{result.type}</span>
                    </div>

                    {selected && (
                      <span
                        className={classNames(
                          'absolute inset-y-0 right-0 flex items-center pr-4',
                          active ? 'text-white' : 'text-indigo-600'
                        )}
                      >
                        <CheckIcon className="h-5 w-5" aria-hidden="true" />
                      </span>
                    )}
                  </>
                )}
              </Combobox.Option>
              </Link>
            ))}
          </Combobox.Options>
        )}
        </>
    } */}
      </div>
    </div>
  )
}
