import Link from 'next/link'
import React, { useState } from 'react'

const Wiki = () => {
    const [recentPages, setRecentPages] = useState([])
    async function insert_page(){
        // Should probably be slug instead of title
        // multiple slugs can exist for the same page title
        let res = await fetch("/api/wiki",{
            method: "POST",
            body: JSON.stringify({
                "title": "Knowledge_Base_Question_Answering (KBQA)",
                "slug": "knowledge_base_question_answering",
                "resource_name":"knowledge_base_question_answering",
                "aliases":"KBQA",
                "description": "Knowledge base question answering (KBQA) aims to answer a question over a knowledge base (KB). [Lan et al., 2021]",
                "related_papers": [
                    {
                        "title": "RNG-KBQA: Generation Augmented Iterative Ranking for Knowledge Base Question Answering",
                        "arxiv_id": "2109.08678",
                        "authors": [],
                        "date": "21 Mar 2022",
                        "paper_url": "https://arxiv.org/pdf/2109.08678.pdf",
                        "code_url": "https://github.com/salesforce/rng-kbqa"
                    },
                    {
                        "title": "A Survey on Complex Knowledge Base Question Answering: Methods, Challenges and Solutions",
                        "arxiv_id": "2105.11644",
                        "authors": [],
                        "date": "25 May 2021",
                        "paper_url": "https://arxiv.org/pdf/2105.11644.pdf",
                        "code_url": null
                    }
                ],
                "datasets": [
                        {
                            "id": "6fca8541-3746-4179-94c4-e018b1e71bcf",
                            "name": "MNIST",
                            "description": "A public-domain dataset compiled by LeCun, Cortes, and Burges containing 60,000 images, each image showing how a human manually wrote a particular digit from 0-9. Each image is stored as a 28x28 array of integers, where each integer is a grayscale value between 0 and 255, inclusive.",
                            "type": "dataset",
                            "full_name": "",
                            "url": "https://paperswithcode.com/dataset/mnist",
                            "sources": [
                                "paperswithcode",
                                "google_ml"
                            ]
                        }
                ],
                "related_concepts":[
                    "Natural Language Generation (NLG)",
                    "Knowledge Base (KB)",
                    "Data-to-Text Generation",
                    "KB-to-text generation"
                ]
                
            
            })
        })
        let data = await res.json()
        console.log(data)
      }
  return (
    <div>
        <div className='p-8'>
            <h1 className='text-lg font-semibold'>Recently Viewed Pages</h1>
            {/* <button onClick={async()=>{
                await insert_page()
            }}>Temp upload page</button> */}

            {recentPages.map((page, index) => 
            <div>
                <Link href={page.url}>
                    <div>{page.title}</div>
                </Link>
            </div>
            )}
        </div>
        <div>

        </div>
    </div>
  )
}

export default Wiki