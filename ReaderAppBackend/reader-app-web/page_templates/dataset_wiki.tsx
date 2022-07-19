import React, { useEffect, useState } from 'react'
import { ArchiveIcon, ChevronDownIcon, ChevronUpIcon, DocumentTextIcon, PhotographIcon, PlusIcon } from '@heroicons/react/solid'
import { useRouter } from 'next/router'
import {
  CodeIcon,
  BookOpenIcon,
  DatabaseIcon
} from '@heroicons/react/solid'
import DatasetCard from '../components/dataset_card'
import Link from 'next/link'
import ReactMarkdown from 'react-markdown'
import { useMediaQuery } from 'usehooks-ts'
import { get_page_styles } from '../lib/helpers/style_queries'
import { css, cx } from '@emotion/css'
import {get_device_size} from '../lib/utils'


const WikiPage = ({ data }) => {
  const [page, setPage] = useState(null)
  const router = useRouter()
  // const [data, setData] = useState(null)
  const [error, setError] = useState(false)
  const [loading, setLoading] = useState(true)
  const [open, setOpen] = useState(false)
 
  var device_size = get_device_size()
  const styles = get_page_styles(device_size)
  console.log(device_size)
  // console.log(isSM)
// md:768
// lg:1024
// xl:1280
// sm:640


//   const styles = (window.innerWidth > window.innerHeight) ? {
//     header: {
//         display: 'flex',
//         justifyContent: 'center',
//     },
//     body: {
//         boxShadow: '0px 0px 5px black',
//         display: 'flex',
//         justifyContent: 'center',
//         flexDirection: 'column'
//     }
// } : {
//     // other styles
// }
  function modality_icon(modality) {
    switch (modality) {
      case 'Texts':
        return <DocumentTextIcon className=' my-auto h-6 w-6 p-0.5 bg-blue-100 rounded-xl hover:bg-blue-200 cursor-pointer mr-2'></DocumentTextIcon>;
      case 'Images':
        return <PhotographIcon className='my-auto h-6 w-6 p-0.5 bg-blue-100 rounded-xl hover:bg-blue-200 cursor-pointer mr-2'></PhotographIcon>
      default:
        return <></>;
    }
  }
  function metrics_dict_to_arr(metrics_dict, metrics) {
    let metrics_arr = []
    for (let index = 0; index < metrics.length; index++) {
      const metric = metrics[index];
      // console.log(metric)
      metrics_arr.push(metrics_dict[metric])
      // metrics_arr.push(metrics_dict[metric])
    }
    return metrics_arr
  }

  console.log(data)

  return (
    <div>
      <>
        <div  

        className={styles.grid + " p-4 md:p-8"}
        >
          <div

            className={styles.infobox} >
            <h1 className='text-3xl font-semibold'>{data.title[0].toUpperCase() + data.title.substring(1)}</h1>
            <div className='p-2 border-2 rounded-xl '>

            <div className='flex mb-2 mt-1'>
              {data.type &&
                <div className='mr-2 bg-blue-300 rounded-lg p-1 my-1 text-sm cursor-pointer'>
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
              {data.homepage &&
                <Link href={data.homepage}>
                  <DatabaseIcon className=' my-auto h-6 w-6 p-0.5 bg-blue-100 rounded-xl hover:bg-blue-200 cursor-pointer mr-2'></DatabaseIcon>
                </Link>
              }
              {data.paper &&
                <Link href={data.paper.url}>
                  <DocumentTextIcon className=' my-auto h-6 w-6 p-0.5 bg-blue-100 rounded-xl hover:bg-blue-200 cursor-pointer mr-2'></DocumentTextIcon>
                </Link>
              }

            </div>
            <div className='flex'>
            {data.modalities && <>
              {/* <h1>Modalities</h1> */}
              <span className='text-lg font-semibold'>Modalities: </span>
              {
                <span className='ml-1 my-auto'>
                  {
                                    data.modalities.map((modality) =>
                                    <span className=''>
                                      {modality_icon(modality)}
                                    </span>
                                  )
                  }
                </span>
              }
            </>
            }
            </div>

            {/* Map Tasks */}


            <h1 className='text-lg font-semibold'>Tasks:</h1>
            <div className="text-gray-500 w-full max-h-40 overflow-scroll py-2 text-left px-2 bg-gray-50 rounded-xl">

              {data.tasks.map((task, index) =>
                <Link href={task.url}>
                  <div className=' text-black font-medium border-b-2 my-1 cursor-pointer'>{task.task}</div>
                </Link>
              )}
            </div>
            </div>

          </div>

          <h1
            className={styles.description + ' ml-2 md:ml-8 lg:ml-8 mt-4 text-base'}><ReactMarkdown>{data.description}</ReactMarkdown>
          </h1>


          {data.sota &&
            <div
            
            className={styles.table}>
              <h1 className='text-xl font-semibold'>State of the Art</h1>
              <table className="w-full">
                <thead className='bg-gray-50'>
                  <tr className=' mx-4'>
                    <th>Model</th>
                    <th>Date</th>
                    {data.sota.metrics.map((metric) =>
                      <th>{metric}</th>
                    )}

                  </tr>
                </thead>
                <tbody className='divide-y divide-gray-200 bg-white'>
                  {data.sota.rows.map((row) =>
                    <tr>
                      <td>{row.model_name}
                      <div className=' inline-block'>
                        {
                          <Link href={row.paper_url}>
                            <DocumentTextIcon className='ml-2 inline-block h-6 w-6 p-0.5 bg-blue-100 rounded-xl hover:bg-blue-200 cursor-pointer mr-2'></DocumentTextIcon>
                          </Link>
                        }
                        {row.code_links.map((code) =>
                          <Link href={code.url}>
                            <CodeIcon className='ml-2 inline-block h-6 w-6 p-0.5 bg-blue-100 rounded-xl hover:bg-blue-200 cursor-pointer mr-2'></CodeIcon>
                          </Link>
                        )}
                        </div>
                      </td>
                      <td>{row.paper_date}</td>
                      {
                        metrics_dict_to_arr(row.metrics, data.sota.metrics).map((metric) =>
                          <td>{metric}</td>
                        )
                        // row.metrics.map((metric)=>
                        // <td>{metric}</td>
                        // )
                      }
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          }

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
