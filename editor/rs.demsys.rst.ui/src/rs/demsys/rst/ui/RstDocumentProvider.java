package rs.demsys.rst.ui;

import java.util.List;

import org.eclipse.core.runtime.CoreException;
import org.eclipse.core.runtime.IProgressMonitor;
import org.eclipse.emf.ecore.EObject;
import org.eclipse.jface.text.IDocument;
import org.eclipse.xtext.EcoreUtil2;
import org.eclipse.xtext.nodemodel.util.NodeModelUtils;
import org.eclipse.xtext.resource.XtextResource;
import org.eclipse.xtext.ui.editor.model.IXtextDocument;
import org.eclipse.xtext.ui.editor.model.XtextDocumentProvider;
import org.eclipse.xtext.util.concurrent.IUnitOfWork;

import rs.demsys.rst.rst.Heading;
import rs.demsys.rst.rst.SimpleTextHeading;

public class RstDocumentProvider extends XtextDocumentProvider {
//	private static final String XTEXT_FORMAT_ACTION_COMMAND_ID = "org.eclipse.xtext.ui.FormatAction";

	private String setUnderline(String underline, int length) {
		char chUnderline = underline.charAt(0);
		
		StringBuffer newUnderline = new StringBuffer(length);
		for (int i = 0; i < length; i++){
			newUnderline.append(chUnderline);
		}
		
		return newUnderline.toString();
	}
	
	public void format(IDocument document)
			throws CoreException {

		IXtextDocument xDocument = (IXtextDocument) document;
		
//		xDocument.modify(
//		    new IUnitOfWork.Void(){
//		       public void process(IXtextResource resource) {
//		    	   EObject root =  state.getContents().get(0);
//		    	   List<Heading> h = EcoreUtil2.getAllContentsOfType(root, Heading.class);
//		       }
//		 });
		
			xDocument.modify(new IUnitOfWork<Void, XtextResource>() {
				@Override
				public java.lang.Void exec(XtextResource state) throws Exception {
					if (!state.getErrors().isEmpty()) {
						return null;
					}
					
					EObject root =  state.getContents().get(0);
					List<Heading> hList = EcoreUtil2.getAllContentsOfType(root, Heading.class);
				
					for (Heading h : hList) {
						if (h.getName() != null) {
							
							int nameLen = NodeModelUtils.getTokenText(NodeModelUtils.getNode(h.getName())).length();
							
							if (h.getUnderline() != null)
								h.setUnderline(setUnderline(h.getUnderline(), nameLen));
							
							if (h.getUnderlineTop() != null)
								h.setUnderlineTop(setUnderline(h.getUnderlineTop(), nameLen));
						}
					}
					
					List<SimpleTextHeading> sthList = EcoreUtil2.getAllContentsOfType(root, SimpleTextHeading.class);					
					
					for (SimpleTextHeading h : sthList) {
						if (h.getName() != null) {
							
							int nameLen = h.getName().length();
							
							if (h.getUnderline() != null)
								h.setUnderline(setUnderline(h.getUnderline(), nameLen));
							
							if (h.getUnderlineTop() != null)
								h.setUnderlineTop(setUnderline(h.getUnderlineTop(), nameLen));
						}
					}
					
					return null;
			    }
			}
			);

	}
	
	@Override
	protected void doSaveDocument(IProgressMonitor monitor, Object element, IDocument document, boolean overwrite)
			throws CoreException {
		// auto-format
//		IHandlerService service = (IHandlerService) PlatformUI.getWorkbench().getService(IHandlerService.class);
//		try {
//			service.executeCommand(XTEXT_FORMAT_ACTION_COMMAND_ID, null);
//		} catch (ExecutionException | NotDefinedException | NotEnabledException | NotHandledException e) {
//			e.printStackTrace();
//		}
		format(document);
		// save
		super.doSaveDocument(monitor, element, document, overwrite);
	}
}
