import React from 'react'
import reactStringReplace from 'react-string-replace';

type Props = {}

const Test = (props: Props) => {


    // function create_page(){
    //     let start_pos = page.body.indexOf("deformable parts models (DPM)")
    // }

    let page = {
        "body" :`
        1 Introduction
Humans glance at an image and instantly know what objects are in the image, where they are, and how they interact. The human visual system is fast and accurate, allowing us to perform complex tasks like driving with little conscious thought. Fast, accurate algorithms for object detection would allow computers to drive cars without specialized sensors, enable assistive devices to convey real-time scene information to human users, and unlock the potential for general purpose, responsive robotic systems.

Current detection systems repurpose classifiers to perform detection. To detect an object, these systems take a classifier for that object and evaluate it at various locations and scales in a test image. Systems like deformable parts models (DPM) use a sliding window approach where the classifier is run at evenly spaced locations over the entire image [10].

More recent approaches like R-CNN use region proposal methods to first generate potential bounding boxes in an image and then run a classifier on these proposed boxes. After classification, post-processing is used to refine the bounding boxes, eliminate duplicate detections, and rescore the boxes based on other objects in the scene [13]. These complex pipelines are slow and hard to optimize because each individual component must be trained separately.
`,
"entities": [{
    "span": "deformable parts models (DPM)",
    "start_pos":749,
    "end_pos":778

}]
    }
    console.log(page.body.indexOf("deformable parts models (DPM)"))
    console.log("deformable parts models (DPM)".length)

    function renderSection(page){
        let jsx
        let char_index =0
        let elements = []
        for (let index = 0; index < page.entities.length; index++) {
            const entity = page.entities[index];
            elements.push(<span className=''>{page.body.substring(index,entity.start_pos)}</span>)
            elements.push(<a className='bg-blue-200 px-1' href={"https://google.com"}>{entity.span}</a>)
            char_index = entity.end_pos
            // If it's the last element add the rest of the text span
            if(index == page.entities.length-1){
                elements.push(<span>{page.body.slice(entity.end_pos)}</span>)
            }
            
        }
        return <div>{elements.map((element)=>element)}</div>
    }
    

  return (
    <div>
        {renderSection(page)}
    </div>
  )
}

export default Test