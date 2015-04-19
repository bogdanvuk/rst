package rs.demsys.rst.formatting2;

import java.util.List;

import rs.demsys.rst.rst.Heading;

import org.eclipse.core.runtime.CoreException;
import org.eclipse.core.runtime.IProgressMonitor;
import org.eclipse.emf.ecore.EObject;
import org.eclipse.jface.text.IDocument;
import org.eclipse.ui.PlatformUI;
import org.eclipse.ui.handlers.IHandlerService;
import org.eclipse.xtext.EcoreUtil2;
import org.eclipse.xtext.ui.editor.model.XtextDocumentProvider;
import org.eclipse.xtext.ui.editor.model.IXtextDocument;
import org.eclipse.xtext.util.concurrent.IUnitOfWork;
import org.eclipse.xtext.resource.XtextResource;

public class RstFormatterHelper {
	
	public static void format(IDocument document)
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
						if ((h.getUnderline() != null) && (h.getName() != null)) {
							int nameLen = h.getName().length();
							int underlineLen = h.getUnderline().length();
							
							if (nameLen != underlineLen) {
							
								char chUnderline = h.getUnderline().charAt(0);
								
								
								StringBuffer newUnderline = new StringBuffer(nameLen);
								for (int i = 0; i < nameLen; i++){
									newUnderline.append(chUnderline);
								}
								
								//newUnderline.append("\n");
								
								h.setUnderline(newUnderline.toString());
							}
						}
					}
					
					return null;
			    }
			}
			);

	}
}