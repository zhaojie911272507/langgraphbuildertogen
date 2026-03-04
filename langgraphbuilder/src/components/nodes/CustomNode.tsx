import { Handle, Position, useReactFlow } from '@xyflow/react'
import type { Node as NodeType, NodeProps } from '@xyflow/react'
import { useCallback, useState, useMemo, useRef, useEffect } from 'react'
import { useButtonText } from '@/contexts/ButtonTextContext'

export type CustomNodeData = {
  label: string
}

export type CustomNode = NodeType<CustomNodeData>

export default function CustomNode({ data, id, selected }: NodeProps<CustomNode>) {
  const { setNodes } = useReactFlow()
  const { buttonTexts, updateButtonText } = useButtonText()
  const [nodeWidth, setNodeWidth] = useState(150)
  const inputRef = useRef<HTMLInputElement>(null)

  const { borderColor: randomBorderColor, backgroundColor: randomBackgroundColor } = useMemo(() => {
    const hue = Math.floor(Math.random() * 360)
    const saturation = 70 + Math.random() * 30
    const lightness = 60 + Math.random() * 20
    const borderColor = `hsl(${hue}, ${saturation}%, ${lightness}%)`

    const lightnessIncrement = 90
    const backgroundLightness = Math.min(lightness + lightnessIncrement, 95)
    const backgroundColor = `hsl(${hue}, ${saturation}%, ${backgroundLightness}%)`

    return { borderColor, backgroundColor }
  }, [])

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newLabel = e.target.value
    updateButtonText(id, newLabel)
    // Update the node label in React Flow
    setNodes((nds: any[]) =>
      nds.map((node) => {
        if (node.id === id) {
          return {
            ...node,
            data: {
              ...node.data,
              label: newLabel,
            },
          }
        }
        return node
      }),
    )

    adjustNodeSize()
  }

  const adjustNodeSize = useCallback(() => {
    if (inputRef.current) {
      const textWidth = inputRef.current.scrollWidth
      const newWidth = Math.max(150, textWidth)
      setNodeWidth(newWidth)
    }
  }, [])

  useEffect(() => {
    updateButtonText(id, data.label)
  }, [])

  useEffect(() => {
    adjustNodeSize()
  }, [buttonTexts[id], adjustNodeSize])

  return (
    <div className='rounded-md p-0' style={{ border: 'none', backgroundColor: 'transparent' }}>
      <div
        className='rounded-md p-2'
        style={{
          border: `2px solid ${randomBorderColor}`,
          backgroundColor: randomBackgroundColor,
          width: `${nodeWidth}px`,
          boxShadow: selected ? '0 0 12px rgba(0, 0, 0, 0.3)' : 'none',
        }}
      >
        <input
          ref={inputRef}
          type='text'
          className='w-full outline-none rounded-md text-center p-0 text-white'
          value={buttonTexts[id]}
          onChange={handleInputChange}
          style={{
            backgroundColor: 'transparent',
            color: '#333333',
            width: '100%',
          }}
        />
        <Handle
          type='source'
          style={{
            width: '10px',
            height: '10px',
            backgroundColor: '#FFFFFF',
            border: `2px solid ${randomBorderColor}`,
          }}
          position={Position.Bottom}
        />
        <Handle
          type='target'
          style={{
            width: '10px',
            height: '10px',
            backgroundColor: '#FFFFFF',
            border: `2px solid ${randomBorderColor}`,
          }}
          position={Position.Top}
        />
      </div>
    </div>
  )
}
