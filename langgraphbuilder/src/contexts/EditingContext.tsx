import React, { createContext, useState, ReactNode } from 'react'

interface EditingContextProps {
  editingEdgeId: string | null
  setEditingEdgeId: (id: string | null) => void
}

export const EditingContext = createContext<EditingContextProps>({
  editingEdgeId: null,
  setEditingEdgeId: () => {},
})

interface EditingProviderProps {
  children: ReactNode
}

export const EditingProvider: React.FC<EditingProviderProps> = ({ children }) => {
  const [editingEdgeId, setEditingEdgeId] = useState<string | null>(null)

  return <EditingContext.Provider value={{ editingEdgeId, setEditingEdgeId }}>{children}</EditingContext.Provider>
}
