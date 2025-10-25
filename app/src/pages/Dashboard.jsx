import React from 'react';
import TransactionCard from '../components/TransactionCard.jsx';
import data from '../data/sampleData.json';
export default function Dashboard(){
  return(
    <div className='p-4 space-y-3'>
      {data.map((txn)=>(<TransactionCard key={txn.txn_id} txn={txn}/>))}
    </div>
  );
}