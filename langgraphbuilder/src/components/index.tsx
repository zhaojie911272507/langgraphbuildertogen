import Flow from './Flow'
import { ReactFlowProvider } from '@xyflow/react'
import { ReactFlowProvider as ReactFlowProviderFlow } from 'reactflow'
import { EdgeLabelProvider } from '@/contexts/EdgeLabelContext'
import { ButtonTextProvider } from '@/contexts/ButtonTextContext'
import { EditingProvider } from '@/contexts/EditingContext'

export default function Page() {
  return (
    <ReactFlowProvider>
      <ReactFlowProviderFlow>
        <ButtonTextProvider>
          <EdgeLabelProvider>
            <EditingProvider>
              <Flow />
            </EditingProvider>
          </EdgeLabelProvider>
        </ButtonTextProvider>
      </ReactFlowProviderFlow>
    </ReactFlowProvider>
  )
}
