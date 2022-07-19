import React, { Fragment, useEffect, useState } from 'react'
import reactStringReplace from 'react-string-replace';
import { MathJax } from 'better-react-mathjax'
import react_parse from 'html-react-parser';
import Link from 'next/link'
import Section from '../../components/section'
import dynamic from "next/dynamic";
import Head from 'next/head'
const PDFViewer = dynamic(() => import("../../components/pdf-view"), {
  ssr: false
});
// import dynamic from 'next/dynamic'
const PaperHTML = ({ doc, parse, references, images,links,paper_id }) => {


  useEffect(()=>{
    console.log(parse)
  },[])


  if(doc){


    var section_titles = []
    // console.log(references)
    // Map array of author's intitution as a row but needs to show the author it corresponds to
    // 
    function get_institutions(authors) {
      let orgs = []
      authors.forEach((author) => {
        if (orgs.includes(author.affiliation.intitution) == false && typeof (author.affiliation.institution) == "string") {
          orgs.push(author.affiliation.institution)
        }
      })
      return orgs
    }
  
    const scroll_to_ref = (ref_id) => {
      console.log(ref_id)
      const section = document.getElementById(ref_id);
      section.scrollIntoView({ behavior: 'smooth', block: 'start' });
    };
  
  
  
    function get_section(paragraphs, num, title) {
      //  
  
  
      // Section title and all paragraphs
      // Paragraphs not in a section considered to be 1.0
      // 
      let render = []
  
      let sec_base_paragraphs = []
  
      let sec_paragraphs = []
      let subsections = []
      let subsections_titles = []
      paragraphs.forEach((p) => {
        if (p.sec_num) {
          if (p.sec_num == num) {
            sec_base_paragraphs.push(p)
          }
  
          if (p.sec_num.startsWith(num.charAt(0))) {
            sec_paragraphs.push(p)
          }
        }
      })
  
      sec_paragraphs.forEach((p) => {
        if (p.sec_num.length == 1) {
          render.push(
            <div>
              <h3>{p.sec_title}</h3>
              <p>{p.content}</p>
            </div>
          )
        }
        if (p.sec_num.length == 3) {
          // Subsection
          // For each subsection get all base paragraphs
  
          let base_paragraphs = []
          // Subsection title, and all paragraphs as an array
          // Get all subsections in subsection
          let sub_paragraphs = []
          sec_paragraphs.forEach((sub_p) => {
            if (sub_p.sec_num.startsWith(p.sec_num)) {
              if (sub_p.sec_num == p.sec_num) {
                base_paragraphs.push(sub_p)
              }
              else {
                sub_paragraphs.push(sub_p)
              }
            }
          })
  
          let sub_sub_section_titles = []
          let sub_sub_sections = []
          sub_paragraphs.forEach((sub_sub_p) => {
            if (sub_sub_section_titles.includes(sub_sub_p.section) == false) {
              sub_sub_section_titles.push(sub_sub_p.section)
            }
          })
  
          sub_sub_section_titles.forEach((sub_sub_section) => {
            let sub_sub_paragraphs = []
            sub_paragraphs.forEach((sub_sub_p) => {
              if (sub_sub_p.section == sub_sub_section) {
                sub_sub_paragraphs.push(sub_sub_p)
              }
            })
  
            if (sub_sub_sections.includes({
              title: sub_sub_section,
              paragraphs: sub_sub_paragraphs
            }) == false) {
              sub_sub_sections.push({
                title: sub_sub_section,
                paragraphs: sub_sub_paragraphs
              })
            }
  
            // console.log(sub_sub_paragraphs)
          })
          let sub_section = {
            title: p.section,
            paragraphs: base_paragraphs,
            subsections: sub_sub_sections
          }
  
          if (subsections_titles.includes(sub_section.title) == false) {
            subsections_titles.push(sub_section.title)
            subsections.push(sub_section)
          }
  
          // console.log("Subparagraphs: ",sub_paragraphs)
  
        }
  
      })
      // console.log("Paragraphs: ",sec_base_paragraphs)
      // console.log("Subsections: ",subsections)
      return {
        title: title,
        paragraphs: sec_base_paragraphs,
        subsections: subsections
      }
    }
    let sections = []
    function initalize_json() {
      let distinct_sections = []
      parse.body_text.forEach((p) => {
        if (p.sec_num) {
          if (p.sec_num.length == 1 && distinct_sections.includes(p.section) == false) {
            distinct_sections.push(p.section)
          }
        }
      })
  
      distinct_sections.forEach((sec, index) => {
        let section = get_section(parse.body_text, (index + 1).toString(), sec)
        sections.push(section)
      })
  
  
    }
    let distinct_sections = []
    let distinct_sec_nums = []
    parse.body_text.forEach((p) => {
      if (p.sec_num) {
        if (distinct_sec_nums.includes(p.sec_num.charAt(0)) == false) {
          distinct_sec_nums.push(p.sec_num.charAt(0))
        }
        if (distinct_sections.includes(p.section) == false) {
          distinct_sections.push(p.section)
        }
      }
    })
    console.log(distinct_sections)
    console.log(distinct_sec_nums)
  
    distinct_sections.forEach((sec, index) => {
      let section_texts = []
      // console.log(sec)
      parse.body_text.forEach((p) => {
        if (p.section == sec) {
          section_texts.push(p)
        }
      })
      sections.push({
        title: sec,
        paragraphs: section_texts
      })
    })
  
    // console.log("Sections: ", sections)
    // initalize_json()
  

    return (
      <div className='p-4 md:p-8 max-w-screen overflow-scroll'>
        <Head>
          <title>{doc.title}</title>
        </Head>
       
          <div>
        {/* Paper Header */}
        <div>
          <h1 className=' font-bold text-2xl'>
            {doc.title}
          </h1>
          <div className='flex'>
            {doc.authors.map((author) =>
              <div className='mr-4 text:md md:text-lg font-semibold'>{author.first} {author.last}</div>
            )}
          </div>
          <div>
            {get_institutions(doc.authors).map((org) =>
              <div>
                <div className='mr-4 font-medium'>{org}</div>
              </div>
            )}
          </div>
          <div className='flex flex-wrap'>
            {doc.authors.map((author) =>
              <a className='mr-4 text-sm font-serif' href={"mailto:" + author.email}>{author.email}</a>
            )}
          </div>
        </div>
  
        {/* Abstract */}
        <div className='my-8'>
          <h1 className='ltx_title ltx_title_section'>{"Abstract"}</h1>
          <div>{doc.abstract}</div>
  
  
        </div>
  
        {/* Paper Body */}
        <div>
          {
          sections.map((section, index) =>{
            if(section.title.includes("::")){
              if(section_titles.includes(section.title.split("::")[0])==false){
                section_titles.push(section.title.split("::")[0])
                let title = section.title
                section.title = section.title.split("::")[1]
                return(
                  <>
                  <h1 className='ltx_title ltx_title_section'>{title.split("::")[0]}</h1>
                  <Section paper_id={paper_id} key={index} data={section} parse={parse} links={links} scroll_to_ref={scroll_to_ref}></Section>
                  </>
                  )
              }
              // If
              if(section.title.split("::").length==3){
                section.title = section.title.split("::")[2]
              }
              else{
                section.title = section.title.split("::")[1]

              }
              return(
                <Section paper_id={paper_id} key={index} data={section} parse={parse} links={links} scroll_to_ref={scroll_to_ref}></Section>
                )
            }
            else{
              // console.log(section.title.split("::")[0])
              return(
                <Section paper_id={paper_id} key={index} data={section} parse={parse} links={links} scroll_to_ref={scroll_to_ref}></Section>
                )
            }

          }
          )}
        </div>
  
        {/* References */}
        <div>
          <h1 className='ltx_title ltx_title_section'>{"References"}</h1>
          <div className='grid grid-cols-2'>
            {references.map((ref, index) => {
              if (Object.keys(ref.other_ids).includes("arXiv")) {
                var arxiv_id = ref.other_ids["arXiv"][0].replace("arXiv:", "")
                var arxiv_pdf_url = "https://arxiv.org/pdf/" + arxiv_id + ".pdf"
                var url = process.env.NEXT_PUBLIC_HOST + "/read/" + arxiv_id
              }
              if (typeof (url) != 'undefined') {
                return (
                  <a target="_blank" href={url} id={ref.ref_id}>
                    <div className='p-4 shadow-md m-4 rounded-xl'>
                      {/* <span>{url}</span> */}
                      <span>{ref.raw_text}</span>
                      {/* <span>{ref.authors.map((author)=>
              <span>{author.first} {author.last}, </span>
              )}.
              </span>
              <span> {ref.year}.</span>
              <span> {ref.title}</span> */}
                    </div>
                  </a>
                )
              }
              else {
                return (
                  <div className='p-4 shadow-md m-4 rounded-xl'>
                    <span>{ref.raw_text}</span>
                    {/* <span>{ref.authors.map((author)=>
              <span>{author.first} {author.last}, </span>
              )}.
              </span>
              <span> {ref.year}.</span>
              <span> {ref.title}</span> */}
                  </div>
                )
              }
  
            }
  
            )}
          </div>
        </div>
        </div>
          
      </div>
    )
  }
  else{
    const [counter, setCounter] = React.useState(0);
  const [numPages, setNumPages] = useState(null);
  const [links, setLinks] = useState(null);
  const [title, setTitle] = useState("Synesthesia Reader");
  const [paper,setPaper] = useState(null)
  
  useEffect(()=>{

    async function fetch_paper() {
      let res = await fetch("/api/paper?arxiv_id="+paper_id)
      var data = await res.json()
      setPaper(data)
      console.log(data.code)
    }
    fetch_paper()
  },[])

  
  function onDocumentLoadSuccess({ numPages }) {
    setNumPages(numPages);
  }
  return (
    <>
      <Head>
        <title>{title}</title>
      </Head>
    
    <div className='h-screen-full text-sm'>

        <>
        <PDFViewer setTitle={setTitle} paper={paper} arxiv_id={paper_id} url={`https://arxiv.org/pdf/${paper_id}.pdf`}></PDFViewer>
        </>
    </div>
    </>
  )
  
  }
  

}

export default PaperHTML

export async function getServerSideProps(context) {
  const {url,id} = context.query
  const arxiv_id = id
  let res = await fetch(process.env.NEXT_PUBLIC_API_URL+"/api/render",{
    method: "POST",
    body: JSON.stringify({url:url,arxiv_id:arxiv_id}),
  })
  
  let data = await res.json()
  if(data.error){
    let res = await fetch(process.env.NEXT_PUBLIC_API_URL+"/api/queue/add",{
      method: "POST",
      body: JSON.stringify({
        arxiv_id:arxiv_id,
        html_rendered:false
      }),
    })
    return {
      props: {
        doc: null,
        parse: null,
        references: null,
        images: null,
        links: null,
        paper_id: arxiv_id
      }
    }
  }
  else{
  return {
    props: {
      doc: data.doc,
      parse: data.parse,
      references: data.references,
      images: data.images,
      links: data.entities,
      paper_id: arxiv_id
    }
  }
}
}




