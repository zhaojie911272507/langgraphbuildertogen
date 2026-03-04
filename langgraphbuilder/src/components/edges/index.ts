import type { BuiltInEdge, Edge, EdgeTypes } from '@xyflow/react'

import ButtonEdge, { type ButtonEdge as ButtonEdgeType } from './ButtonEdge'
import SelfConnectingEdge from './SelfConnectingEdge'
export const initialEdges = [
  // { id: 'a->c', source: 'a', target: 'c', animated: true },
  // { id: 'b->d', source: 'b', target: 'd', type: 'button-edge' },
  // { id: 'c->d', source: 'c', target: 'd', animated: true },
] satisfies Edge[]

export const edgeTypes = {
  'button-edge': ButtonEdge,
  'self-connecting-edge': SelfConnectingEdge,
} satisfies EdgeTypes

// Append the types of you custom edges to the BuiltInEdge type
export type CustomEdgeType = BuiltInEdge | ButtonEdgeType
