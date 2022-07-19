import React, { useEffect, useState } from 'react'
import react_parse from 'html-react-parser';
import fs from 'fs';
import Script from 'next/script'
import { Html, Main, NextScript } from 'next/document'
import dynamic from "next/dynamic";
import Head from 'next/head'
import {
  CodeIcon,
  BookOpenIcon,
  DatabaseIcon
} from '@heroicons/react/solid'
const PDFViewer = dynamic(() => import("../../components/pdf-view"), {
  ssr: false
});
const ReadPaper = ({ html, arxiv_id }) => {
  const [counter, setCounter] = React.useState(0);
  const [numPages, setNumPages] = useState(null);
  const [links, setLinks] = useState(null);
  const [title, setTitle] = useState("Synesthesia Reader");
  const [paper,setPaper] = useState(null)
  
  useEffect(()=>{

    async function fetch_paper() {
      let res = await fetch("/api/paper?arxiv_id="+arxiv_id)
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
      {html ? react_parse(html, {
        replace: (domNode) => {
          try {
            if (domNode.name === "img") {
              console.log(domNode.attribs.src)
              let source = `https://synesthesia-research.s3.us-east-2.amazonaws.com/papers/${arxiv_id}/figures/${domNode.attribs.src}`
              return <img src={source} />
            }

          } catch (error) {
            //  console.log(error)
          }
        }
      }) :
        <>
        <PDFViewer setTitle={setTitle} paper={paper} arxiv_id={arxiv_id} url={`https://arxiv.org/pdf/${arxiv_id}.pdf`}></PDFViewer>
        </>
      }

    </div>
    </>
  )
}

export default ReadPaper

ReadPaper.whyDidYouRender = false

import { cwd } from 'process';
import { parse } from 'node-html-parser';
import { MongoClient } from 'mongodb'
import Link from 'next/link';
export async function getServerSideProps(context) {
  const { id } = context.query;
  const regex = /^\d{4}\.\d{4,5}$/;
  if (regex.test(id)) {
    const uri = "mongodb://diego:twyvW7z9bRJ9OFQM@165.232.156.229";
    const mongo_client = new MongoClient(uri);
    console.log(id)

    renderedHTML = null
    await mongo_client.connect();
    const database = mongo_client.db('research_papers');
    const extracted_papers = database.collection('reader_renders');
    const queue = database.collection('queue');
    var paper = await extracted_papers.findOne({
        "arxiv_id": id
      })
      if (paper) {
        var renderedHTML = paper.html
        var images = paper.images
        console.log(images)
      }
      else{
        queue.insertOne({
          arxiv_id: id,
          base_processed:true,
          html_rendered:false
        })
      }

      
  }
  else {
    var renderedHTML = null
  }
  return {
    props: {
      html: renderedHTML,
      arxiv_id: id,
    }
  }
}