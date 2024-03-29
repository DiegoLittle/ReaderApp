/*
  This example requires Tailwind CSS v2.0+ 
  
  This example requires some changes to your config:
  
  ```
  // tailwind.config.js
  module.exports = {
    // ...
    plugins: [
      // ...
      require('@tailwindcss/forms'),
    ],
  }
  ```
*/
import { useEffect, useState } from 'react'
import { CheckIcon, SelectorIcon } from '@heroicons/react/solid'
import { Combobox } from '@headlessui/react'
import Link from 'next/link'

const people = [
  { id: 1, name: 'Leslie Alexander' },
  // More users...
]

function classNames(...classes) {
  return classes.filter(Boolean).join(' ')
}

export default function Example({setQuery,search}) {
  const [results,setResults] = useState({})
  const [selectedPerson, setSelectedPerson] = useState()
  const [toggles, setToggles] = useState()
  const[paperSelected,setPaperSelected] = useState(false)
  // useEffect(async ()=>{
  //   console.log(query)
  //   try {
  // //     
  //     let res = await fetch(process.env.NEXT_PUBLIC_HOST+'/api/paper_search?q='+query)
  //     let data = await res.json()
  //     setResults(data)
  //     console.log(data)
  //     console.log(results)
  //   } catch (error) {
  //     console.log(error)
  //   }


  // },[query])

//   const filteredPeople =
//     query === ''
//       ? people
//       : people.filter((person) => {
//           return person.name.toLowerCase().includes(query.toLowerCase())
//         })

  return (
    <div className={"lg:mx-32"} >
      {/* <Combobox.Label className="block text-sm font-medium text-gray-700">Assigned to</Combobox.Label> */}
      <div className="relative mt-1">
        <label className='flex text-center font-semibold my-8 text-2xl justify-center'>Search for a paper</label>
        <div className="flex w-2/3 lg:w-1/2 mx-auto rounded-lg border border-gray-300 bg-white py-1 pl-1 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 sm:text-sm">
          <div 
          onClick={()=>{
            console.log(paperSelected)
            setPaperSelected(!paperSelected)
          }}
          className={` rounded-lg p-1  inline-flex cursor-pointer ${paperSelected ? "bg-blue-300 hover:bg-blue-400":"bg-blue-100 hover:bg-blue-200"}`}>Papers</div>
        
        <input
        className='w-full focus:outline-none ml-1'
        onKeyDown={(e)=>{
          if(e.key==='Enter'){
            if (paperSelected){
              search("papers")
            }
            else{
              search()
            }
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
