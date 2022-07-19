import { randomUUID } from 'crypto';
import { NextApiRequest, NextApiResponse } from 'next';
import { getSession } from 'next-auth/react';
import {prisma} from '../../lib/prisma';
export default async (req:NextApiRequest, res:NextApiResponse) => {
    console.log("Getting session")
    const session = await getSession({ req })

    console.log(req.query)
    let {title,url} = req.query
    console.log(title)
    console.log(url)
    let user = await prisma.user.findFirst({
        where:{
            email: session.user.email
        }
    })
    let add_BM = await prisma.bookmarks.create({
        data:{
            id: randomUUID(),
            title:title,
            url:url,
            type:"web",
            description:"",
            User:{
                connect:{
                    id: user.id
                }
            }
        }
    })
    res.json(add_BM)

    req.statusCode = 200

}