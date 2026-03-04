import React, { createContext, useState, useContext } from 'react'

type EdgeLabelContextType = {
  edgeLabels: { [sourceNodeId: string]: string }
  updateEdgeLabel: (sourceNodeId: string, label: string) => void
  getEdgeLabel: (sourceNodeId: string, defaultLabel: string) => string
}

const EdgeLabelContext = createContext<EdgeLabelContextType | undefined>(undefined)

export const EdgeLabelProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [edgeLabels, setEdgeLabels] = useState<{ [sourceNodeId: string]: string }>({})

  const updateEdgeLabel = (sourceNodeId: string, label: string) => {
    setEdgeLabels((prev) => ({ ...prev, [sourceNodeId]: label }))
  }

  const getEdgeLabel = (sourceNodeId: string, defaultLabel: string) => {
    return edgeLabels[sourceNodeId] || defaultLabel
  }

  return (
    <EdgeLabelContext.Provider value={{ edgeLabels, updateEdgeLabel, getEdgeLabel }}>
      {children}
    </EdgeLabelContext.Provider>
  )
}

export const useEdgeLabel = () => {
  const context = useContext(EdgeLabelContext)
  if (context === undefined) {
    throw new Error('useEdgeLabel must be used within an EdgeLabelProvider')
  }
  return context
}
