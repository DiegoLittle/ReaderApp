// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import type { NextApiRequest, NextApiResponse } from 'next'
type Data = {
  name: string
}
// const PDFParser = require("pdf2json");

// const pdfParser = new PDFParser();
export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<Data>
) {
    const {arxiv_id } = req.query
    let fetch_res = await fetch("http://localhost:8000/api/papers/cso?arxiv_id=" + arxiv_id)
    let data = await fetch_res.json()
    // console.log(data)
    if(data){
    let entities_ = data.entities
    let entities = []
    for (let i = 0; i < entities_.length; i++) {
        let entity = entities_[i]
        let new_entity = JSON.parse(entity)
        new_entity.pages = []
        entities.push(new_entity)
    }
    data.entities = entities
  
    return res.json(data)
  }
  return res.json({error:"No document found"})
}