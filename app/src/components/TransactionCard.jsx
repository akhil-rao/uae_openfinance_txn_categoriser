import React from 'react';
export default function TransactionCard({txn}){
  return(
  <div className='bg-white shadow-md rounded-2xl p-3'>
    <div className='flex justify-between'>
      <h3 className='font-semibold'>{txn.matched_merchant}</h3>
      <span className='text-sm text-gray-600'>{txn.l2_vertical}</span>
    </div>
    <p className='text-gray-500 text-sm'>{txn.description_raw}</p>
    <div className='mt-2'>
      <div className='h-2 bg-gray-200 rounded-full'>
        <div className='h-2 bg-green-500 rounded-full' style={{width:`${txn.confidence*100}%`}}></div>
      </div>
      <p className='text-xs text-gray-400 mt-1'>Confidence: {txn.confidence}</p>
    </div>
  </div>);
}