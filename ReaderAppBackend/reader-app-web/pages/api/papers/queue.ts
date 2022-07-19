import { NextApiRequest, NextApiResponse } from 'next';
import { mongo_client } from '../../../lib/mongo_methods';

export default async (req:NextApiRequest, res:NextApiResponse) => {

    let body = JSON.parse(req.body)

    let url = body.url
    let html_rendered = body.html_rendered
    let arxiv_id = body.arxiv_id
    await mongo_client.connect();
    const database = await mongo_client.db('research_papers');
    const queue = await database.collection('queue');
    // var insert_res = await queue.replaceOne({
    //     "url": url,
    //     "html_rendered": html_rendered,
    //     "arxiv_id": arxiv_id
    // },{
    //     "url": url,
    //     "html_rendered": html_rendered,
    //     "arxiv_id": arxiv_id
    // },{
    //     upsert: true
    // })
    var update_res = await queue.updateOne({
        "arxiv_id": arxiv_id
    },{
        $set: {
            "html_rendered": html_rendered
        }
    },{
        upsert: true
    })


    return res.json({
        "status": "Added to queue"
    })





}