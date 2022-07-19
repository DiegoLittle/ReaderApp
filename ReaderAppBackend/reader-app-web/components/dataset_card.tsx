import { DatabaseIcon } from '@heroicons/react/solid'
import Link from 'next/link'
import React from 'react'
import LinesEllipsis from 'react-lines-ellipsis'

const DatasetCard = ({dataset}) => {
  return (
    
        <Link href={"/wiki/"+dataset.name}>
            <div className='my-4 shadow-md  p-2 rounded-lg cursor-pointer'>
    <div className='text-lg font-semibold'>{dataset.name}</div>
    <div>{dataset.date}</div>
    {/* <div>{dataset.description}</div> */}
    <LinesEllipsis
    text={dataset.description}
    maxLine='3'
    ellipsis='...'
    trimRight
    basedOn='letters'
    />
    <div className='flex my-2'>
      {dataset.url &&
        <Link href={dataset.url}>
          <DatabaseIcon className='h-6 w-6 p-0.5 bg-blue-100 rounded-xl hover:bg-blue-200 cursor-pointer mr-2'></DatabaseIcon>
        </Link>
      }
      {/* {paper.paper_url &&
        <Link href={paper.paper_url}>
          <BookOpenIcon className='h-6 w-6 p-0.5 bg-blue-100 rounded-xl hover:bg-blue-200 cursor-pointer mr-2'></BookOpenIcon>
        </Link>
      } */}
    </div>
    </div>
    </Link>
  
  )
}

export default DatasetCard