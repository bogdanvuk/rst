package rs.demsys.rst.ui.spelling;

import static rs.demsys.rst.ui.spelling.RstTerminalsTokenTypeToPartitionMapper.TEXT_PARTITION;

import org.eclipse.xtext.ui.editor.model.PartitionTokenScanner;

public class RstPartitionTokenScanner extends PartitionTokenScanner {
	@Override
	protected boolean shouldMergePartitions(String contentType) {
		return super.shouldMergePartitions(contentType)
				|| TEXT_PARTITION.equals(contentType);
	}
}
