package rs.demsys.rst.ui.spelling;

import static rs.demsys.rst.ui.spelling.RstTerminalsTokenTypeToPartitionMapper.TEXT_PARTITION;

import org.eclipse.jface.text.BadLocationException;
import org.eclipse.jface.text.IDocument;
import org.eclipse.jface.text.ITypedRegion;
import org.eclipse.jface.text.source.ISourceViewer;
import org.eclipse.xtext.ui.editor.reconciler.XtextSpellingReconcileStrategy;

public class RstSpellingReconcileStrategy extends
		XtextSpellingReconcileStrategy {

	private IDocument fDocument;
	
	public static class factory extends XtextSpellingReconcileStrategy.Factory {
		@Override
		public XtextSpellingReconcileStrategy create(ISourceViewer sourceViewer) {
			return new RstSpellingReconcileStrategy(sourceViewer);
		}
	}
	
	protected RstSpellingReconcileStrategy(ISourceViewer viewer) {
		super(viewer);
	}

	@Override
	public void setDocument(IDocument document) {
		super.setDocument(document);
		fDocument = document;
	}
	
	@Override
	protected boolean shouldProcess(ITypedRegion typedRegion) {
		if (super.shouldProcess(typedRegion)
				|| TEXT_PARTITION.equals(typedRegion.getType())) {
			String word;
			try {
				word = fDocument.get(typedRegion.getOffset(), typedRegion.getLength());
				if (word.indexOf('-') == -1)
					return true;
			} catch (BadLocationException e) {
				// TODO Auto-generated catch block
				return false;
			}
		}
		return false;
	}
}
