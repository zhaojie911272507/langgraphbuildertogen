import type { BuiltInNode, Node, NodeTypes } from '@xyflow/react'
import PositionLoggerNode, { type PositionLoggerNode as PositionLoggerNodeType } from './PositionLoggerNode'
import SourceNode, { type SourceNode as SourceNodeType } from './SourceNode'
import CustomNode, { type CustomNode as CustomNodeDataType } from './CustomNode'
import EndNode, { type EndNode as EndNodeType } from './EndNode'

export const initialNodes = [
  // { id: 'a', type: 'input', position: { x: 0, y: 0 }, data: { label: 'wire' } },
  // {
  //   id: 'b',
  //   type: 'position-logger',
  //   position: { x: -100, y: 100 },
  //   data: { label: 'drag me!' },
  // },
  // { id: 'c', position: { x: 100, y: 100 }, data: { label: 'your ideas' } },
  {
    id: 'source',
    type: 'source',
    position: { x: 0, y: 0 },
    data: { label: 'start' },
  },
  {
    id: 'end',
    type: 'end',
    position: { x: 0, y: 600 },
    data: { label: '__end__' },
  },
] satisfies Node[]

export const nodeTypes = {
  'position-logger': PositionLoggerNode,
  source: SourceNode,
  custom: CustomNode,
  end: EndNode,
} satisfies NodeTypes

// Append the types of you custom edges to the BuiltInNode type
export type CustomNodeType = BuiltInNode | PositionLoggerNodeType | SourceNodeType | CustomNodeDataType | EndNodeType
