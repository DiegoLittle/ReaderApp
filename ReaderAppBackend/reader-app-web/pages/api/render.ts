import { NextApiRequest, NextApiResponse } from 'next'
const { Pool, Client } = require('pg')
import { mongo_client } from '../../lib/mongo_methods'

export default async (req: NextApiRequest, res: NextApiResponse) => {
  req.statusCode = 200
  await mongo_client.connect()
  const database = await mongo_client.db('research_papers')
  const docs = await database.collection('doc_jsons')
  const queue = await database.collection("queue")
  const text = 'SELECT entity_links FROM papers where arxiv_id = $1'
  const { url, arxiv_id } = JSON.parse(req.body)
  console.log(url, arxiv_id)
  const client = await new Client({
    user: process.env.PG_USER,
    host: process.env.PG_HOST,
    database: process.env.PG_DATABASE,
    password: process.env.PG_PASSWORD,
    port: process.env.PG_PORT,
    idleTimeoutMillis: 30000,
  })
  client.connect()
  const db_res = await client.query(text, [arxiv_id])
  var item = db_res.rows[0]
  // console.log(item)
  if(typeof(item) != 'undefined'){
  if(item.entity_links == null){
    var entities = []
    // Update queue to add entities to the paper
  //   queue.insertOne({
  //     arxiv_id: arxiv_id,
  //     entity_links_processed: false,
  //     priority: 1
  // })
  }
  else{
    var entities = item.entity_links.map((link)=>
    JSON.parse(link)
    )
    
  }
}
    // console.log(entities)

  if (typeof url != 'undefined') {
    var doc_res = await docs.findOne({
      url: url,
    })
  } else if (typeof arxiv_id != 'undefined') {
    var doc_res = await docs.findOne({
      paper_id: arxiv_id,
    })
  }
  if (doc_res) {
    delete doc_res._id
  }else{
    
    return res.json({error:"No document found"})
  }
  // let doc = doc_res
  // doc._id = id
  await mongo_client.close()
  let doc = doc_res

  let is_latex = Object.keys(doc).includes('latex_parse')
  let is_pdf = Object.keys(doc).includes('pdf_parse')
  if (is_pdf) {
    var parse = doc.pdf_parse
    delete doc.pdf_parse
  } else if (is_latex) {
    var parse = doc.latex_parse
    delete doc.latex_parse
  }
  async function match_figures(figures) {
    let unmatched_figures = []
    let figure_image_files = []
    Object.keys(parse.ref_entries).forEach((entry) => {
      if (entry.startsWith('FIGREF')) {
        // console.log(entry)
        let ref_entry = parse.ref_entries[entry]
        if (ref_entry.uris.length == 0) {
          // console.log(ref_entry.text)
          unmatched_figures.push({
            id: entry,
            text: ref_entry.text,
          })
        }
      }
    })
    figures.forEach((figure_item) => {
      figure_image_files.push(
        figure_item
          .split('/')
          [figure_item.split('/').length - 1].replaceAll('_', ' ')
          .replace('.png', '')
      )
    })
    // console.log(unmatched_figures)
    // console.log(figure_image_files)
    let sim_res = await fetch('http://localhost:8001/api/similarity', {
      method: 'POST',
      body: JSON.stringify({
        q: unmatched_figures[0],
        elements: figure_image_files,
      }),
    })
    let sim_res_json = await sim_res.json()
    // console.log(sim_res_json)
    // console.log(sim_res_json['top_element'])
    let top_elem = sim_res_json['top_element']
    parse.ref_entries[unmatched_figures[0].id].uris.push()
    let ref_id = unmatched_figures[0].id

    return {
      ref_id: 'figures/' + top_elem.replaceAll(' ', '_') + '.png',
    }
    // console.log(parse)
  }

  let temp_entries = []
  // console.log(parse)
  Object.keys(parse.bib_entries).map((key) => {
    temp_entries.push(parse.bib_entries[key])
  })
  console.log("Test")


  // const data = await match_figures(doc.figures)
  // console.log("Test")
  return res.json( {
      doc: doc_res,
      parse: parse,
      references: temp_entries,
      images: [],
      entities: entities,  })
}
