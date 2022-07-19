import React, { useEffect, useState } from 'react'
import DatasetCard from '../../../components/dataset_card'
const Datasets = () => {
  const [datasets, setDatasets] = useState(null)
    useEffect(()=>{
        async function fetchData() {
            let res = await fetch("/api/wiki/datasets")
            var data = await res.json()
            setDatasets(data)

        }
        fetchData()
        
    },[])
  return (
    <div className=''>
      <div className='grid grid-cols-3 '>
      {datasets && datasets.map((dataset) =>
      <div className='m-4'>
        <DatasetCard dataset={dataset}></DatasetCard>
        </div>
        )}
      </div>
    </div>
  )
}

export default Datasets