import { CodeIcon, DocumentTextIcon } from '@heroicons/react/solid'
import Link from 'next/link'
import React from 'react'

const EvaluationTable = ({ sota }) => {

    function metrics_dict_to_arr(metrics_dict, metrics) {
        let metrics_arr = []
        for (let index = 0; index < metrics.length; index++) {
            const metric = metrics[index];
            // console.log(metric)
            metrics_arr.push(metrics_dict[metric])
            // metrics_arr.push(metrics_dict[metric])
        }
        return metrics_arr
    }

    return (
        <div>
            <table className="w-full">
                <thead className='bg-gray-50'>
                    <tr className=' mx-4'>
                        <th>Model</th>
                        <th>Date</th>
                        {sota.metrics.map((metric) =>
                            <th>{metric}</th>
                        )}

                    </tr>
                </thead>
                <tbody className='divide-y divide-gray-200 bg-white'>
                    {sota.rows.map((row) =>
                        <tr>
                            <td>{row.model_name}
                                <div className=' inline-block'>
                                    {
                                        <Link href={row.paper_url}>
                                            <DocumentTextIcon className='ml-2 inline-block h-6 w-6 p-0.5 bg-blue-100 rounded-xl hover:bg-blue-200 cursor-pointer mr-2'></DocumentTextIcon>
                                        </Link>
                                    }
                                    {row.code_links.map((code) =>
                                        <Link href={code.url}>
                                            <CodeIcon className='ml-2 inline-block h-6 w-6 p-0.5 bg-blue-100 rounded-xl hover:bg-blue-200 cursor-pointer mr-2'></CodeIcon>
                                        </Link>
                                    )}
                                </div>
                            </td>
                            <td>{row.paper_date}</td>
                            {
                                metrics_dict_to_arr(row.metrics, sota.metrics).map((metric) =>
                                    <td>{metric}</td>
                                )
                                // row.metrics.map((metric)=>
                                // <td>{metric}</td>
                                // )
                            }
                        </tr>
                    )}
                </tbody>
            </table>
        </div>
    )
}

export default EvaluationTable