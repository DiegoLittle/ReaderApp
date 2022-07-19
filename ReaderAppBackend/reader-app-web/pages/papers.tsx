import type { NextPage } from 'next'
import Head from 'next/head'
import Image from 'next/image'
import { useEffect, useRef, useState } from 'react'
import PaperCard from '../components/paperCard'
import Header from '../components/msHeader'
import useOnScreen from '../lib/hooks/useOnScreen'
import { useIntersectionObserver } from 'usehooks-ts'
function classNames(...classes) {
  return classes.filter(Boolean).join(' ')
}

const Home: NextPage = () => {
  const [papers, setPapers] = useState<Paper[]>([])
  const [selectedCategories, setSelectedCategories] = useState<string[]>([])
  // const paperCardRef = useRef(null)
  async function onLastPaperVisible() {
    console.log('last paper visible')
  }
  useEffect(()=>{

    async function fetch_papers(){
      console.log('Home page loaded')
      let papers = await fetch('/api/papers')
      papers = await papers.json()
      console.log("Papers: ", papers)
      // console.log(papers)
      setPapers(papers)
    }
    fetch_papers()
  },[])
  
  const main_cats = ["Computer Vision and Pattern Recognition","Machine Learning","Computation and Language","Artificial Intelligence","Neural and Evolutionary Computing","Robotics"]
  

  return (
    <div className="flex min-h-screen flex-col ">
      {/* <Header></Header> */}
      {/* <div className='py-4 bg-red-500 w-full px-8 mx-8'>
        <ToggleButton></ToggleButton>
      </div> */}
      <div>
        <div className='flex mt-8 mr-auto items-start justify-start md:mx-6 overflow-scroll'>
          {main_cats.map((cat,i)=>
          <div onClick={()=>{
            setSelectedCategories((prev)=>{
              if(prev.includes(cat)){
                let new_prev = prev.filter((c)=>c!==cat)
                return new_prev
              }
              else{
                return [...prev,cat]
              }
              // if(prev.includes(cat)=>{
              //   let new_prev = prev.filter((c)=>c!==cat)
              //   return new_prev
              // })
              // else{
              //   return [...prev,cat]
              // }
            })
          }} 
          className={classNames(
            selectedCategories.includes(cat) ? 'bg-blue-200 hover:bg-blue-300' : 'bg-blue-50 hover:bg-blue-100 ',
            'text-sm cursor-pointer font-semibold rounded-xl px-2 py-1 mx-2'
          )}
          // className={`  ${selectedCategories.includes(cat)?"bg-blue-200":""}`}
          >{cat}</div>
          )}
        </div>
        {selectedCategories.map((e)=><div>{e}</div>)}
      </div>
      <main className="flex w-full flex-1 flex-col ">
        {papers.map((paper,index) => 
        <>
        {index==papers.length-1?<PaperCard setPapers={setPapers} papers={papers} paper={paper}></PaperCard>
        :<PaperCard setPapers={null} paper={paper}></PaperCard>}
        </>
          
        )}
      </main>
    </div>
  )
}

export default Home


import { Switch } from '@headlessui/react'

function ToggleButton() {
  const [enabled, setEnabled] = useState(false)
  const defaultSizes={
    "bg_h":19,
    "bg_w":37,
    "circle_h":17,
    "circle_w":17,
  }
  var sizeFactor = 1
  return (
    <div className="">
      <Switch
        checked={enabled}
        onChange={setEnabled}
        className={`${enabled ? 'bg-teal-900' : 'bg-teal-700'}
          relative inline-flex h-[${defaultSizes.bg_h * sizeFactor}px] w-[${defaultSizes.bg_w * sizeFactor}px] shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus-visible:ring-2  focus-visible:ring-white focus-visible:ring-opacity-75`}
      >
        <span className="sr-only">Use setting</span>
        <span
          aria-hidden="true"
          className={`${enabled ? 'translate-x-4' : 'translate-x-0'}
            pointer-events-none inline-block h-[${defaultSizes.circle_h * sizeFactor}px] w-[${defaultSizes.circle_w * sizeFactor}px] -translate-y-[1px] transform rounded-full bg-white shadow-lg ring-0 transition duration-200 ease-in-out`}
        />
      </Switch>
    </div>
  )
}
