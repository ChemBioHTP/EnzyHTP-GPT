import React from 'react'
import "./style.css"
import TileContent from '../TileContent/TileContent'
import { ReactComponent as Line } from '../../../../assets/images/RunSimulation/Line 16.svg';

const Workflow = () => {
  return (
    <>
    <div className='TileContent'>
        <TileContent header="Structure Preparation" description="Remove water, loop fixing, protonate."/>
    </div>
    <Line/>
    <div className='TileContent'>
        <TileContent header="Structure operation" description="Coordinate manipulation, mutation."/>
    </div>
    <Line/>
    <div className='TileContent'>
        <TileContent header="Conformation exploration" description="MD simulation"/>
    </div>
    <Line/>
    <div className='TileContent'>
        <TileContent header="Energy calculation" description="QM/MM..."/>
    </div>
    </>
  )
}

export default Workflow