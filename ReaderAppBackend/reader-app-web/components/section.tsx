import React, { memo,Fragment, useState } from 'react'
import reactStringReplace from 'react-string-replace';
import { MathJax } from 'better-react-mathjax'
import HighlightPop from 'react-highlight-pop';

function Section({ data, parse, scroll_to_ref,links,paper_id }) {

  let annotation_types = [
    "Dataset","Task","Method","Metric","Model"
  ]
  const [newAnnotations, setNewAnnotations] = useState([])
  const [selectedText, setSelectedText] = useState('')
  var test = ""
  
    function ref_element(BIBREF) {
      return (
        <a href={"#" + BIBREF} className='text-blue-400 cursor-pointer hover:text-blue-500'
          onClick={() => {
            console.log("Hello World")
          }}>
          {`(${parse.bib_entries[BIBREF].authors[0].last} et al., ${parse.bib_entries[BIBREF].year})`}
        </a>
      )
    }
    function replace_bibitems_regex(text) {
      console.log(text)
      // let re = new RegExp("BIBREF/d")
      let re = /BIBREF\d\d|BIBREF\d/g
      let matches = text.match(re)
      console.log("Matches: ", matches)
      if (matches) {
        matches.forEach((match) => {
          text = reactStringReplace(text, match, (match, i) => {
            return ref_element(match)
          })
        })
      }
      return text
    }
  
    function inline_latex(ref_id,eq_spans){
      let latex
      for (let index = 0; index < eq_spans.length; index++) {
        const span = eq_spans[index];
        if(span.ref_id == ref_id){
          latex = span.latex
          break
        }
      }
      return latex
    }
  
    function replace_elements(p, parse) {
  
      p.ref_spans.forEach((span) => {
        p.text = reactStringReplace(p.text, span.ref_id, (match, i) => {
          // console.log(match,i,span.ref_id)
          if (span.ref_id.startsWith("TAB")) {
            // console.log(parse.ref_entries[span.ref_id])
            console.log("Render table")
            // parse.ref_entries[span.ref_id].content.forEach((row) => {
            //   // console.log(row.cells)
            // })
            return (
              <div className="overflow-scroll">
                <h1>{replace_bibitems_regex(parse.ref_entries[span.ref_id].text)}</h1>
                <table className="divide-y divide-gray-300 overflow-scroll">
                  <tbody className="divide-y divide-gray-200 bg-white">
                    {parse.ref_entries[span.ref_id].content.map((row) => (
                      <tr >
                        {row.cells.map((cell) =>
                          <td className="whitespace-nowrap text-sm font-medium text-gray-900 sm:pl-6">
                            {cell.text}
                          </td>
                        )}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )
  
            // return(
            //   <div>
            //     <h1>{react_parse(parse.ref_entries[span.ref_id].text)}</h1>
            //   {react_parse(parse.ref_entries[span.ref_id].html)}
            //   </div>
            // )
          }
          else if (span.ref_id.startsWith("SEC")) {
            // console.log(span.ref_id)
            // Section refs
  
          }
          else if (span.ref_id.startsWith("FIG")) {
            // console.log(parse.ref_entries[span.ref_id])
            // console.log(span.ref_id)
            // console.log("Figure")
            if (parse.ref_entries[span.ref_id].uris.length > 0) {
              var uri = parse.ref_entries[span.ref_id].uris[0].split("/")[1].replace(".pdf", "")
              let image_url = "https://synesthesia-research.s3.us-east-2.amazonaws.com/papers/"+paper_id+"/figures/" + uri + ".png"
              return (
                <img src={image_url}></img>
              )
            }
  
  
            return (
              <span>{match}</span>
            )
          }
          else if (span.ref_id.startsWith("EQ")) {
            return (
              <span>{<MathJax inline={true}>{`\\(${parse.ref_entries[span.ref_id].latex}\\)`}</MathJax>}</span>
            )
          }
        })
      })
  
      p.cite_spans.forEach((span) => {
        // console.log(span.ref_id)
        // p.text = reactStringReplace(p.text, span.ref_id, (match, i) => (
        //   <span>{ref_element(span.ref_id)}</span>
        // ));
        p.text = reactStringReplace(p.text, span.ref_id, (match, i) => {
          if (span.ref_id.length < 8) {
            // console.log(span.ref_id)
            // console.log(p.text)
  
          } else {
  
          }
          return (
            <span>{ref_element(span.ref_id)}</span>
          )
        })
      })
      p.eq_spans.forEach((span) => {
        // console.log(span)
        // BIBREF2 is matching for BIBREF22
        p.text = reactStringReplace(p.text, span.ref_id, (match, i) => {
          // console.log(match,i,span.ref_id)
          return (
            <span>{<MathJax inline={true}>{`\\(${span.latex}\\)`}</MathJax>}</span>
          )
        })
      })
      return p
    }
    function get_title(){

    }
    let footnotes = []
    return (
      <HighlightPop
      onHighlightPop={(text)=>{
        setSelectedText(text)
        // test = text
      }}
      popoverItems={itemClass => {

        return (
        <Fragment>
          {annotation_types.map((type)=>
                     <span 
                     className="text-blue-500 mx-2 cursor-pointer" onClick={() => {
                      //  alert(selectedText)
                       setNewAnnotations((prev)=>
                          [...prev,selectedText]
                       )
                     }}>
                     {type}
                 </span>
          )}

        </Fragment>
       )}
      }
      >
      <div className='ltx_section '>
        {/* {newAnnotations.map((annotation)=>
        <div>{annotation}</div>
        )} */}
        <h1 className=' font-semibold text-lg'>{data.title}</h1>
        {data.paragraphs.map((p) => {

          p.ref_spans.forEach((span)=>{
            if(Object.keys(span).includes("ref_id")){
            if(span.ref_id.startsWith("FOOTREF")){
              parse.ref_entries[span.ref_id].ref_id=span.ref_id
              footnotes.push(parse.ref_entries[span.ref_id])
            }
          }
          
          })
          // p = replace_elements(p, parse)
          let elements = []
          let re = /BIBREF\d\d|BIBREF\d|INLINEFORM\d|FIGREF\d\d|FIGREF\d|SECREFU\d\d|SECREFU\d|SECREF\d|SECREF\d\d|EQREF\d\d|EQREF\d|TABREF\d\d|TABREF|ENTITY\d\d\d|ENTITY\d\d|ENTITY\d|FOOTREF\d\d|FOOTREF\d/g
          let matches = p.text.match(re)
          // console.log(matches)
          if (matches) {
            p.text.split(/BIBREF\d\d|BIBREF\d|INLINEFORM\d|FIGREF\d\d|FIGREF\d|SECREFU\d\d|SECREFU\d|SECREF\d|SECREF\d\d|EQREF\d\d|EQREF\d|TABREF\d\d|TABREF\d|ENTITY\d\d\d|ENTITY\d\d|ENTITY\d|FOOTREF\d\d|FOOTREF\d/g).forEach((element, i) => {
              elements.push(element)
              if (matches.length >= i) {
                if (typeof (matches[i]) != 'undefined') {
                  elements.push(matches[i])
                }
              }
            })
            // console.log(elements)
            return (
              <div className='ltx_para'><p className='ltx_p'>{
                elements.map((element) => {
                  if (element.startsWith("BIBREF")) {
                    return (
                      <a href={"#" + element} className='text-blue-400 cursor-pointer hover:text-blue-500'
                        onClick={() => {
                          console.log("Hello World")
                        }}>
                          <span>(</span>
                          {typeof(parse.bib_entries[element]) != 'undefined' &&
                            <>
                          {typeof(parse.bib_entries[element].authors[0])!='undefined'&&
                          <span>{parse.bib_entries[element].authors[0].last + " et al."}</span>}

                          {parse.bib_entries[element].year&&
                          <span>, {parse.bib_entries[element].year}</span>
                          }
                        </>
                        }
                          <span>)</span>
                      </a>
                    )
                  }
                  else if(element.startsWith("INLINEFORM")){
                    // console.log(element)
                    // console.log(p)
                    // console.log(inline_latex(element,p.eq_spans))
                    return(
                      // <span></span>
                      <span>{<MathJax inline={true}>{`\\(${inline_latex(element,p.eq_spans)}\\)`}</MathJax>}</span>
                    )
                  }
                  else if(element.startsWith("FIGREF")){
                    // console.log(parse.ref_entries)
                    // console.log(element)
                    if(typeof(parse.ref_entries[element]) != 'undefined'){
                    if (parse.ref_entries[element].uris.length > 0) {
                      console.log(parse.ref_entries)
                      try{
                      var uri = parse.ref_entries[element].uris[0].split("/")[1].replace(".pdf", "")
                    }
                    catch{
                      console.log(parse.ref_entries[element].uris[0].split("/"))
                    }
          
                      let image_url = "https://synesthesia-research.s3.us-east-2.amazonaws.com/papers/"+paper_id+"/figures/" + uri + ".png"
                      return (
                        <img src={image_url}></img>
                      )
                    }
                  }
                  }
                  else if(element.startsWith("SECREF")){
  
                  }
                  else if(element.startsWith("EQ")){
                    return(
                      <span>{<MathJax inline={true}>{`\\(${parse.ref_entries[element].latex}\\)`}</MathJax>}</span>
                    )
                  }
                  else if(element.startsWith("FOOTREF")){
                    console.log(p)
                    return(
                     <a href={"#"+element}> <sup>{element.replace("FOOTREF","")}</sup></a>
                    )
                  }
                  else if(element.startsWith("TAB")){
                    console.log("Render table")
                    // parse.ref_entries[span.ref_id].content.forEach((row) => {
                    //   // console.log(row.cells)
                    // })
                    if(typeof(parse.ref_entries[element]) != 'undefined'){
                    return (
                      <div className="overflow-scroll">
                        {/* <h1>{replace_bibitems_regex(parse.ref_entries[span.ref_id].text)}</h1> */}
                        <table className="divide-y divide-gray-300 overflow-scroll">
                          <tbody className="divide-y divide-gray-200 bg-white">
                            {parse.ref_entries[element].content.map((row) => (
                              <tr >
                                {row.cells.map((cell) =>
                                  <td className="whitespace-nowrap text-sm font-medium text-gray-900 sm:pl-6">
                                    {cell.text}
                                  </td>
                                )}
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    )
                  }else{
                    console.log(parse.ref_entries[element])
                  }
                  }
                  else if(element.startsWith("ENTITY")){
                    if(typeof(parse.entity_entries[element]) != 'undefined'){
                      // console.log(parse.entity_entries[element])
                      if(typeof(parse.entity_entries[element].link.url) != 'undefined'){
                        var url = parse.entity_entries[element].link.url
                      }
                      else{
                        var url = process.env.NEXT_PUBLIC_HOST+"/wiki/"+parse.entity_entries[element].link.name
                      }
                      return(
                        <a href={url} className="text-blue-500 hover:text-blue-600">{parse.entity_entries[element].span}</a>
                      )
                    }
  
                  }
                  else{
                    // console.log(textRenderer(element,links))
                    newAnnotations.forEach((annotation)=>{
                      
                      if(typeof(element)=="string"){
                        
                        if(element.includes(annotation)){
                          console.log(annotation)
                          console.log(element)
                          element = reactStringReplace(element,annotation,(match,i)=>(
                            <a className="text-blue-500 hover:text-blue-600">{match}</a>
                          ))
                        }
                      }
                      else{
                        console.log(annotation)
                        console.log(element)
                        for (let index = 0; index < element.length; index++) {
                          const jsx_item = element[index];
                          if(typeof(jsx_item)=="string"){
                            if(jsx_item.includes(annotation)){
                              console.log(annotation)
                              console.log(element)
                              element = reactStringReplace(element,annotation,(match,i)=>(
                                <a className="text-blue-500 hover:text-blue-600">{match}</a>
                              ))
                              console.log(element)
                            }
                          }
                        }
                      }

                    })
                    return(
                      <span>{element}</span>
                    )
                  }
                }
                )}
              </p></div>
  
            )
          } else {
            return (
              <div className='ltx_para'><p className='ltx_p'>{p.text}</p></div>
            )
          }
        }
        )}
        {footnotes.map((footnote)=>{
          // console.log(footnote)
          return(
        <div id={footnote.ref_id} className="italic text-sm">
          <sup>{footnote.ref_id.replace("FOOTREF","")}</sup>{footnote.text}
        </div>
        )
        }
        )}
        {data.subsections && data.subsections.map((subsection) =>
          <>
            <div className='font-semibold text-xl'>{subsection.title}</div>
            {subsection.paragraphs.map((p) => {
              p = replace_elements(p, parse)
              return (
                <div className='ltx_para'><p className='ltx_p'>{p.text}</p></div>)
            }
            )}
            {subsection.subsections.map((subsection) =>
              <div>
                <div className='font-medium text-lg'>{subsection.title}</div>
                {subsection.paragraphs.map((p) => {
                  p = replace_elements(p, parse)
                  return (
                    <div className='ltx_para'><p className='ltx_p'>{p.text}</p></div>
  
                  )
                }
                )}
              </div>
            )}
          </>
        )}
      </div>
      </HighlightPop>
    )
  }

export default memo(Section)