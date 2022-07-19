import { NextApiRequest, NextApiResponse } from 'next';
import { mongo_client } from '../../../lib/mongo_methods'

export default async (req:NextApiRequest, res:NextApiResponse) => {
    
    const {arxiv_id,html_rendered} = JSON.parse(req.body)
    await mongo_client.connect()
    const database = await mongo_client.db('research_papers')
    const queue = database.collection('queue');
    const insert_res = await queue.updateOne({
        arxiv_id: arxiv_id,
    },{
        $set: {
            html_rendered: html_rendered,
            priority: 1
        }
    },{
        upsert: true
    }
    )
    
    await mongo_client.close()
    if(insert_res.acknowledged){
        res.json({success:true})
    }
    else{
        res.json({error:"Could not add to queue"})
    }

    req.statusCode = 200


}