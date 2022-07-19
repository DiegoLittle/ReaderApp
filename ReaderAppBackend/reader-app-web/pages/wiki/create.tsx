import React, { useState } from 'react'

const Create = () => {
    const [term, setTerm] = useState('');
    const [termType, setTermType] = useState('');
    return (
        <div>
            <div className='p-4 md:p-8'>
                <div>Name</div>
                <input
                    className='focus:outline-none ml-1 inline-flex border-2 rounded-lg p-1 focus:border-blue-200'
                    onKeyDown={(e) => {
                    }}
                    autoComplete='off'
                    onChange={(event) => {
                        setTerm(event.target.value)
                    }
                    }
                />
                <div>Type</div>
                <SelectTermType type={termType} setType={setTermType}></SelectTermType>
                <div>Paper URL</div>
                <input
                    className='focus:outline-none ml-1 inline-flex border-2 rounded-lg p-1 focus:border-blue-200'
                    onKeyDown={(e) => {
                    }}
                    autoComplete='off'
                    onChange={(event) => {
                        setTerm(event.target.value)
                    }
                    }
                />

            </div>
        </div>
    )
}

export default Create




function SelectTermType({type,setType}){
return (
    <div className='w-1/4 grid grid-cols-2'>
    <div
        onClick={async () => {
            setType("dataset")
        }}
        className={`text-center p-1 m-1 cursor-pointer rounded-lg ${type == 'dataset' ? 'bg-blue-400 hover:bg-blue-300' : "bg-blue-50 hover:bg-blue-200"}`}>Dataset</div>
    <div
        onClick={async () => {
            setType("task")
        }}
        className={`text-center p-1 m-1 cursor-pointer rounded-lg ${type == 'task' ? 'bg-blue-400 hover:bg-blue-300' : "bg-blue-50 hover:bg-blue-200"}`}>Task</div>
    <div
        onClick={async () => {
            setType("method")
        }}
        className={`text-center p-1 m-1 cursor-pointer rounded-lg ${type == 'method' ? 'bg-blue-400 hover:bg-blue-300' : "bg-blue-50 hover:bg-blue-200"}`}>Method</div>
    <div
        onClick={async () => {
            setType("metric")
        }}
        className={`text-center p-1 m-1 cursor-pointer rounded-lg ${type == 'metric' ? 'bg-blue-400 hover:bg-blue-300' : "bg-blue-50 hover:bg-blue-200"}`}>Metric</div>
     <input onChange={(e) => {
         setType(e.target.value)
        // setAnnotationType(e.target.value)
    }}
        className='focus:outline-1 outline-blue-200 p-1 pl-4 placeholder-gray-500 m-1 cursor-pointer rounded-lg bg-blue-50  ' placeholder='label'></input>
    <div
        onClick={async () => {
            setType("Custom")
        }}
        className='text-center p-1 m-1 cursor-pointer rounded-lg bg-blue-50 hover:bg-blue-200'>Custom</div>
</div>
)
}