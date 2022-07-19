import React, { useState, useRef, useEffect, forwardRef, memo } from 'react'
import { Document, Page } from 'react-pdf/dist/esm/entry.webpack5';
import react_parse from 'html-react-parser';
// import samplePDF from './sample.pdf';
import dynamic from "next/dynamic";
import { useTextSelection } from 'use-text-selection'
import { Dialog, Transition } from '@headlessui/react'
import { Fragment } from 'react'
import { CodeIcon, XCircleIcon, XIcon } from '@heroicons/react/solid';
import { useIntersectionObserver } from 'usehooks-ts';
import { useSelector,useDispatch } from 'react-redux';
import {selectPdfPage, SelectPdfPage,addPageIndexToEntities} from '../store/slices/pdfPageSlice'
import { setCurrentPage,setLinksRedux } from '../store/slices/pdfPageSlice';


const Popover = dynamic(() => import('react-text-selection-popover').then((module) => module.Popover), {
  ssr: false
});


const PDFView = ({ url, setTitle, paper, arxiv_id }) => {
  const dispatch = useDispatch()
  const [numPages, setNumPages] = useState(1);
  // let samplePDF = 'https://arxiv.org/pdf/2205.02830.pdf'
  const [selectedText, setSelectedText] = useState('')
  const [annotationType, setAnnotationType] = useState(null)
  const [links, setLinks] = useState(null)
  const [shiftClick, setShiftClick] = useState(false)
  const ref = useRef()
  const entry = useIntersectionObserver(ref, {})
  const isVisible = !!entry?.isIntersecting
  const [totalPages, setTotalPages] = useState(null)

  useEffect(() => {
    async function fetch_entities() {
      let res = await fetch("/api/entity_lookup?arxiv_id=" + arxiv_id)
      var data = await res.json()
      // console.log(data)
      console.log(data.entities)
      dispatch(setLinksRedux(data.entities))
      setLinks(data.entities)
    }
    fetch_entities()

  }, [])


  function onSelectionChange() {
    const selection = document.getSelection();
  }
  function onDocumentLoadSuccess({ numPages }) {
    setTotalPages(numPages)
  }

  async function add_annotation(annotation) {

    await fetch("/api/add_annotation", {
      method: "POST",
      body: JSON.stringify(annotation)
    })
  }


  function removeTextLayerOffset() {
    console.log("Removing text layer offset")

    // pageRef.current.addEventListener("click", (e) => {
    //   console.log(e)
    // });
    // document.addEventListener("selectionchange", onSelectionChange);
    document.addEventListener("keydown", (e) => {
      if (e.key == "Shift") {
        setShiftClick(true)
      }
    })
    document.addEventListener("keyup", (e) => {
      if (e.key == "Shift") {
        setShiftClick(false)
      }
    })

    const textLayers = document.querySelectorAll(".react-pdf__Page__textContent");
    textLayers.forEach(layer => {
      const { style } = layer;
      style.top = "0";
      style.left = "0";
      style.transform = "";
    });
  }

  // pdfViewer.container.addEventListener("keyup", this.onKeyUp);
  // pdfViewer.container.addEventListener("scroll", this.onViewportChanged);
  // console.log(add);

  useEffect(() => {
    if (isVisible) {
      // onInView()
      console.log("In view")
      console.log("paper visible")
      // setNumPages(numPages+1)
    }
    // console.log("isVisible: ", isVisible)
  }, [isVisible])

  function get_elements(str,link){
    var elements = []
            let start_pos = str.indexOf(link.span)
            let end_pos = start_pos+link.span.length
            // console.log(str)
            console.log(start_pos)
            console.log(str)
    console.log("---------------")
    console.log(str.substring(0,start_pos))
    console.log(link.span)
    console.log(str.slice(end_pos))
    console.log("---------------")

    var entity_element = <a href={`${link.link.url}`} target="_blank" className="relative border-2 cursor-pointer border-blue-400 bottom-1">{link.span}</a>
    elements.push(<span>{str.substring(0,start_pos)}</span>)
    // console.log(str.substring(0,))
    elements.push(entity_element)
    // console.log(entity_element)
    // console.log(link.link.name)
    elements.push(<span>{str.slice(end_pos)}</span>)
    return elements
  }
  const textRenderer = (render) => {
    // console.log(render.page)
    // console.log("RenderingText")
    // console.log(render.str)
    var entities_found = []
    var str = render.str
    var includes_kw = false;
    var jsx_element = <span>{str}</span>

    var elements = []

    // link.pages = [0,1,2,3]

    function replace_cskgs(str, link) {
      let found_entities = []
      var element = <span>{str}</span>
      // console.log(link.span)

      // Span likely to be an acronym
      if (link.span.toUpperCase() == link.span) {
        // console.log(link.span)
        //  only replace if the acronym is an exact match
        if (link.link.name.toUpperCase() == link.span) {
          // console.log("ACRONYM")
          str = str.replace(link.span, `<a href=/wiki/${link.link.name} target="_blank" className="relative border-2 cursor-pointer border-red-400 bottom-1">${link.link.name}</a>`)
          // element = <a href={`/wiki/${link.link.name}`} target="_blank" className="relative border-2 cursor-pointer border-red-400 bottom-1">{link.link.name}</a>
          found_entities.push(link.link.name)
        }
      }


      else {
        found_entities.push(link.link.name)
        str = str.replace(link.span, `<a href=/wiki/${link.link.name} target="_blank" className="relative border-2 cursor-pointer border-red-400 bottom-1">${link.link.name}</a>`)
        // element = <a href={`/wiki/${link.link.name}`} target="_blank" className="relative border-2 cursor-pointer border-red-400 bottom-1">{link.link.name}</a>
      }
      return {
        str: str,
        entities: found_entities,
        element: element
      }
    }
    {
      links &&
      // loops through all entities
      links.forEach((link,index) => {
        // if entity type is resource

        // if (link.link.type == "resource") {
          

        //   let cskgs_replaces = replace_cskgs(str, link)
        //   entities_found.concat(cskgs_replaces.entities)
        //   str = cskgs_replaces.str
        //   // jsx_element = cskgs_replaces.element


        //   // console.log(link.link.name)
        // }
        // else {
         
        // }

      })
    }
    // console.log(render)
    // entities_found
    if (entities_found.length > 0 ){
      dispatch(addPageIndexToEntities({
        entities: entities_found,
        page: render.page._pageIndex
      }))
    }
    if(elements.length > 0 ){
      console.log("Elements")
      console.log(elements)
      jsx_element = <span>{elements.map((element)=>element)}</span>

    }
    return jsx_element
    // else {
    //   return (<span onClick={() => { console.log("Hello World") }}>{str}</span>)
    // }

    
    // if (includes_kw) {

    //   // return (<span className='relative border border-blue-100 bottom-1'>{str}</span>)

    //   // It would proabably to try to use jsx directory instead of the react_parse

    // }
    

  }

  return (
    <>
    <SideMenu 
    add_annotation={add_annotation}
    paper={paper}
    selectedText={selectedText}
    setAnnotationType={setAnnotationType}
    url={url}

    ></SideMenu>

      <div



        className='mx-auto w-full justify-center lg:flex'>
        <DocumentView
          url={url}
          onDocumentLoadSuccess={onDocumentLoadSuccess}
          totalPages={totalPages}
          setSelectedText={setSelectedText}
          textRenderer={textRenderer}
          removeTextLayerOffset={removeTextLayerOffset}
        >

        </DocumentView>

      </div>
    </>
  )
}

export default PDFView



const PageView = memo(({ setSelectedText, textRenderer, removeTextLayerOffset, index }) => {
  const ref = useRef<HTMLDivElement | null>(null)
  const entry = useIntersectionObserver(ref, {})
  const isVisible = !!entry?.isIntersecting
  const dispatch = useDispatch()
  console.log(`Render Section ${index+1}`, { isVisible })
  if (isVisible) {
    console.log(`Page ${index+1} is visible`)
    dispatch(setCurrentPage(index+1))
  }
  return (
    <div


      ref={ref}
      onMouseUp={(e) => {
        setSelectedText(window.getSelection().toString())
      }}

    >



      <Page

        customTextRenderer={(str,itemIndex)=>{
          var pageIndex = index+1
          // console.log(pageIndex)
          // console.log(str)
          return textRenderer(str)
        }}
        className="text-center justify-center mx-auto"
        width={1000}
        onLoadSuccess={removeTextLayerOffset}
        renderAnnotationLayer={false}
        key={`page_${index + 1}`}
        pageNumber={index + 1}
      />
    </div>
  )
})

const DocumentView = memo(({ url, onDocumentLoadSuccess, totalPages, setSelectedText, textRenderer, removeTextLayerOffset }) => {
  // Only render pages that have been visible with some offset
  const pdfPage = useSelector(selectPdfPage)
  
  return (
    <Document
      file={url}
      onLoadSuccess={onDocumentLoadSuccess}
    >
      {Array.from(
        new Array(pdfPage.currentPage+1),
        (el, index) => (
          <PageView
            index={index}
            setSelectedText={setSelectedText}
            textRenderer={textRenderer}
            removeTextLayerOffset={removeTextLayerOffset}

          ></PageView>
        )
      )}
    </Document>
  )
})


const SideMenu = ({paper,selectedText,add_annotation,url,setAnnotationType}) => {
  const pdfPage = useSelector(selectPdfPage)
  

  return ( 
    <div className='invisible bg-white lg:visible sticky w-48 pb-2 shadow-lg rounded-xl top-1/4 ml-8 z-10'>
    <h1>Current Page: {pdfPage.currentPage}</h1>
    {/* {links} */}
    <h1 className='mx-auto text-center px-2 pt-1 text-lg font-semibold'>Code</h1>
    {paper &&
      <div className='mx-2'>
        {paper.code && <>
          {Array.isArray(paper.code) ? paper.code.map((code) =>
            <a target="_blank" href={code.repo_url}>
              <CodeIcon className='h-8 w-8 m-2 bg-blue-200 hover:bg-blue-300 cursor-pointer rounded-lg p-1' />
            </a>
          ) :
            <a target="_blank" href={paper.code.repo_url}>
              <CodeIcon className='h-8 w-8 m-2 bg-blue-200 hover:bg-blue-300 cursor-pointer rounded-lg p-1' />
            </a>
          }
        </>}
      </div>
    }

    <h1 className='mx-auto text-center px-2 pt-1 text-lg font-semibold'>Label annotations</h1>
    <div className='text-center p-1'>{selectedText}</div>
    <div className=' grid grid-cols-2'>
      <div
        onClick={async () => {

          await add_annotation({
            name: selectedText,
            type: "dataset",
            sources: [url]
          })
        }}
        className='text-center p-1 m-1 cursor-pointer rounded-lg bg-blue-50 hover:bg-blue-200'>Dataset</div>
      <div
        onClick={async () => {
          console.log(selectedText)
          await add_annotation({
            name: selectedText,
            type: "dataset",
            sources: [url],
          })
        }}
        className='text-center p-1 m-1 cursor-pointer rounded-lg bg-blue-50 hover:bg-blue-200'>Task</div>
      <div
        onClick={async () => {

          await add_annotation({
            name: selectedText,
            type: "method",
            sources: [url]
          })
        }}
        className='text-center p-1 m-1 cursor-pointer rounded-lg bg-blue-50 hover:bg-blue-200'>Method</div>
      <div
        onClick={async () => {

          await add_annotation({
            name: selectedText,
            type: "metric",
            sources: [url]
          })
        }}
        className='text-center p-1 m-1 cursor-pointer rounded-lg bg-blue-50 hover:bg-blue-200'>Metric</div>
    </div>
    <div
      className='flex w-full'>

      <input onChange={(e) => {
        setAnnotationType(e.target.value)
      }}
        className='w-2/3 focus:outline-1 outline-blue-200 p-1 pl-4 placeholder-gray-500 m-1 cursor-pointer rounded-lg bg-blue-50  ' placeholder='label'></input>
      <div
        onClick={async () => {

          await add_annotation({
            name: selectedText,
            type: annotationType,
            sources: [url]
          })
        }}
        className='w-1/3 text-center p-1 m-1 cursor-pointer rounded-lg bg-blue-50 hover:bg-blue-200'>Custom</div>
    </div>
    <h1 className='mx-auto text-center px-2 pt-1 text-lg font-semibold'>Current Page Annotations</h1>
    <div className=' max-h-40 overflow-scroll'>
    {pdfPage.links && pdfPage.links.map((link) => 
    <>
    <div className='flex overflow-scroll '>
    {link.pages.includes(pdfPage.currentPage) && 
      <div className="text-center my-1 bg-blue-100 rounded-lg inline-flex p-1 justify-center mx-auto">
      {link.span}
      <XIcon className='w-4 h-4 my-auto cursor-pointer'></XIcon>
    
    </div>
    }
    </div>
    </>
    )}
    </div>

  </div>
  )
}

const MyModal = forwardRef(({ isOpen, setIsOpen, position }, ref) => {
  function closeModal() {
    setIsOpen(false)
  }

  function openModal() {
    setIsOpen(true)
  }

  return (
    <>
      <div className="fixed inset-0 flex items-center justify-center">
        <button
          type="button"
          onClick={openModal}
          className="rounded-md bg-black bg-opacity-20 px-4 py-2 text-sm font-medium text-white hover:bg-opacity-30 focus:outline-none focus-visible:ring-2 focus-visible:ring-white focus-visible:ring-opacity-75"
        >
          Open dialog
        </button>
      </div>

      <Transition appear show={isOpen} as={Fragment}>
        <Dialog as="div" className="relative z-10" onClose={closeModal}>
          <Transition.Child
            as={Fragment}
            enter="ease-out duration-300"
            enterFrom="opacity-0"
            enterTo="opacity-100"
            leave="ease-in duration-200"
            leaveFrom="opacity-100"
            leaveTo="opacity-0"
          >
            <div className="fixed inset-0 bg-black bg-opacity-25" />
          </Transition.Child>

          <div className="fixed inset-0 overflow-y-auto">
            <div ref={ref} style={
              {
                bottom: position.bottom,
                left: position.left,
                right: position.right,
                top: position.top
              }
            } className={` min-h-full items-center justify-center p-4 text-center`}>
              <Transition.Child
                as={Fragment}
                enter="ease-out duration-300"
                enterFrom="opacity-0 scale-95"
                enterTo="opacity-100 scale-100"
                leave="ease-in duration-200"
                leaveFrom="opacity-100 scale-100"
                leaveTo="opacity-0 scale-95"
              >
                <Dialog.Panel className="w-full max-w-md transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all">
                  <Dialog.Title
                    as="h3"
                    className="text-lg font-medium leading-6 text-gray-900"
                  >
                    Payment successful
                  </Dialog.Title>
                  <div className="mt-2">
                    <p className="text-sm text-gray-500">
                      Your payment has been successfully submitted. We’ve sent
                      you an email with all of the details of your order.
                    </p>
                  </div>

                  <div className="mt-4">
                    <button
                      type="button"
                      className="inline-flex justify-center rounded-md border border-transparent bg-blue-100 px-4 py-2 text-sm font-medium text-blue-900 hover:bg-blue-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
                      onClick={closeModal}
                    >
                      Got it, thanks!
                    </button>
                  </div>
                </Dialog.Panel>
              </Transition.Child>
            </div>
          </div>
        </Dialog>
      </Transition>
    </>
  )
})



const popOverBad = () => {
  return (
    <Popover

      render={
        ({ clientRect, isCollapsed, textContent }) => {
          if (clientRect == null) return null
          // if (isCollapsed){

          // }
          console.log(isCollapsed)
          setIsSelecting(true)
          const left = clientRect.x - containerRef.current.offsetLeft;
          const top = clientRect.y - containerRef.current.offsetTop;
          console.log("Selection: ", selection)
          console.log("ClientRect: ", clientRect)
          console.log(selection.left)
          // const style = css`
          //   position: absolute;
          // left: ${clientRect.left + clientRect.width / 2}px;
          // top: ${clientRect.top - 40}px;
          //   margin-left: -75px;
          //   width: 150px;
          //   background: blue;
          //   font-size: 0.7em;
          //   pointer-events: none;
          //   text-align: center;
          //   color: white;
          //   border-radius: 3px;
          // `
          const width = selection.right - selection.left;
          const height = selection.bottom - selection.top;
          const rotateY = width < 0 ? -180 : 0;
          const rotateX = height < 0 ? -180 : 0;
          // const rgbColor = hexToRgb(color);
          // const border = getBorderWidthFromBounds(bounds);
          // console.log(clientRect)
          console.log("Width: " + selection.right / 2)
          return <div

            style={{
              position: 'absolute',
              left: selection.left + clientRect.width / 2,
              top: selection.top,
              // width: `${Math.abs(width)}px`,
              // height: `${Math.abs(height)}px`,
              // transform: `rotateY(${rotateY}deg) rotateX(${rotateX}deg)`,
              // transformOrigin: 'top left',
              // position: 'absolute',
              // left: clientRect.left + (clientRect.width / 2) - 40,
              // top: clientRect.top + 80,
              // marginLeft: -75,
            }}

            onClick={() => {
              console.log("clicked")
            }}
            className={`absolute cursor-pointer w-[150px] bg-blue-500 rounded-lg p-2 top-full z-10`}>
            Selecting { } characters
          </div>
        }
      }
    />
  )
}