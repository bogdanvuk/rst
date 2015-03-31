package rs.demsys.rst.ui.contentassist

import com.google.inject.Inject
import java.util.ArrayList
import java.util.Arrays
import java.util.List
import org.eclipse.core.resources.IContainer
import org.eclipse.core.resources.IFile
import org.eclipse.core.resources.IResource
import org.eclipse.core.resources.IWorkspaceRoot
import org.eclipse.core.resources.ResourcesPlugin
import org.eclipse.core.runtime.CoreException
import org.eclipse.core.runtime.IPath
import org.eclipse.core.runtime.Path
import org.eclipse.emf.ecore.resource.Resource
import org.eclipse.jface.text.contentassist.ICompletionProposal
import org.eclipse.xtext.Assignment
import org.eclipse.xtext.ui.PluginImageHelper
import org.eclipse.xtext.ui.editor.contentassist.ContentAssistContext
import org.eclipse.xtext.ui.editor.contentassist.ICompletionProposalAcceptor
import rs.demsys.rst.rst.BibDirective
import rs.demsys.rst.rst.ImageDirective
import rs.demsys.rst.rst.IncludeDirective
import org.eclipse.xtext.ui.editor.contentassist.ICompletionProposalAcceptor.Delegate
import org.eclipse.xtext.ui.editor.contentassist.ConfigurableCompletionProposal
import org.eclipse.emf.ecore.EObject

/** 
 * See https://www.eclipse.org/Xtext/documentation/304_ide_concepts.html#content-assist
 * on how to customize the content assistant.
 */
class RstProposalProvider extends AbstractRstProposalProvider {
	@Inject PluginImageHelper imageHelper
	//	@Inject
	//	private IContainer.Manager manager;
	//
	//	@Inject
	//	private IResourceServiceProvider.Registry rspr;
	//
	//	@Inject
	//	private ResourceDescriptionsProvider resourceDescriptionsProvider;
	//
	//	private IResourceDescription.Manager getManager(Resource res) {
	//		IResourceServiceProvider resourceServiceProvider = rspr
	//				.getResourceServiceProvider(res.getURI());
	//		return resourceServiceProvider.getResourceDescriptionManager();
	//	}
	
	static class RefProposalDelegate extends Delegate {
		
		ContentAssistContext ctx;
	
        new(ICompletionProposalAcceptor delegate, ContentAssistContext cctx) {
        	super(delegate);
            this.ctx = cctx;
		}
 
        def override public void accept(ICompletionProposal proposal) {
            if (proposal instanceof ConfigurableCompletionProposal) {
            	val p = proposal as ConfigurableCompletionProposal;
           	
                val endPos = p.replacementOffset + p.replacementLength; 
                if (ctx.getDocument() != null && ctx.getDocument().getLength() > endPos) {
                	
					if (!"`_".equals(ctx.getDocument().get(endPos, 2))) {
					    // We are not at the end of the file
					    p.replacementLength = p.replacementLength + 2;
					    p.replacementString = p.replacementString + "`_";
					    p.cursorPosition = p.cursorPosition + 2;
					}
                }
            }
            super.accept(proposal);
        }
 
    }
	
	def private void acceptFileNameProposals(Resource resource, ContentAssistContext context, ICompletionProposalAcceptor acceptor, List<String> exts, String fileName){
		var ArrayList<String> fileProp=new ArrayList<String>() 
		var ArrayList<String> folderProp=new ArrayList<String>() 
		findFileNameProposals(resource, fileProp, folderProp, exts, fileName) for (String f : folderProp) {
			var ICompletionProposal proposal=createCompletionProposal('''«f»/''', f, imageHelper.getImage("folder.gif"), context) 
			acceptor.accept(proposal) 
		}
		for (String f : fileProp) {
			var ICompletionProposal proposal=createCompletionProposal(f, f, imageHelper.getImage("rst_file.png"), context) 
			acceptor.accept(proposal) 
		}
		
	}
	def private static void findFileNameProposals(Resource resource, ArrayList<String> fileProp, ArrayList<String> folderProp, List<String> exts, String fileName){
		var String platformString=resource.getURI().trimSegments(1).toPlatformString(true) 
		var IFile curFile=ResourcesPlugin.getWorkspace().getRoot().getFile(new Path(platformString))
		
		recursiveFindFileNameProposals(fileProp, folderProp, exts, fileName, curFile.location, curFile, ResourcesPlugin.getWorkspace().getRoot()) 
	}
	
	def private static boolean checkExtension(IResource iR, List<String> exts)
	{
		for (String ext : exts) {
			if (ext.equalsIgnoreCase(iR.getFileExtension())) {
				return true;
			}
		}
		
		return false;
	}
	
	def private static void recursiveFindFileNameProposals(ArrayList<String> fileProp, ArrayList<String> folderProp, List<String> exts, String fileName, IPath path, IFile rootFile, IWorkspaceRoot myWorkspaceRoot){
		var IContainer container=myWorkspaceRoot.getContainerForLocation(path)
//		var fileNameRelative = rootFile.projectRelativePath.append(fileName).toString
		 
		try {
			var IResource[] iResources 
			iResources=container.members() for (IResource iR : iResources) {
				// for c files
				var IPath irPath=iR.projectRelativePath
				var String resRelative=irPath.toString().substring(rootFile.projectRelativePath.toString.length + 1)
//				iR.projectRelativePath
//				resRelative=resRelative.substring(resRelative.indexOf("/", resRelative.indexOf("/") + 1) + 1)
				 
				var boolean resContainsFileName=false 
				var boolean fileNameContainsRes=false 
				if (fileName == null) {
					resContainsFileName=true fileNameContainsRes=false 
				} else {
					resContainsFileName=(resRelative.indexOf(fileName) == 0) fileNameContainsRes=(fileName.indexOf(resRelative) == 0) 
				}if (iR.getType() == IResource.FOLDER) {
					if (resContainsFileName) {
						folderProp.add(resRelative) 
					} else if (fileNameContainsRes) {
						recursiveFindFileNameProposals(fileProp, folderProp, exts, fileName, iR.getLocation(), rootFile, myWorkspaceRoot) 
					}
					
				} else if (resContainsFileName && checkExtension(iR, exts)) {
					fileProp.add(resRelative) /* FIXME Unsupported BreakStatement: */
				}
			}
			
		} catch (CoreException e) {
			// TODO Auto-generated catch block
			e.printStackTrace() 
		}
		
	}
	
	override void completeLongReference_Ref(EObject model, Assignment assignment, ContentAssistContext context, ICompletionProposalAcceptor acceptor) {
		super.completeLongReference_Ref(model, assignment, context, new RefProposalDelegate(acceptor, context));
	}
	
	def void completeBibDirective_Bib(BibDirective model, Assignment assignment, ContentAssistContext context, ICompletionProposalAcceptor acceptor){
		super.completeBibDirective_Bib(model, assignment, context, acceptor) var String fileName=model.getBib() 
		var Resource resource=model.eResource() 
		if (resource != null) {
			acceptFileNameProposals(resource, context, acceptor, Arrays.asList("bib"), fileName) 
		}
		
	}
	
	def void completeImageDirective_Picture(ImageDirective model, Assignment assignment, ContentAssistContext context, ICompletionProposalAcceptor acceptor){
		super.completeImageDirective_Picture(model, assignment, context, acceptor) var String fileName=model.getPicture() 
		var Resource resource=model.eResource() 
		if (resource != null) {
			acceptFileNameProposals(resource, context, acceptor, Arrays.asList("jpg", "png", "pdf", "gif"), fileName) 
		}
		
	}
	
	def void completeIncludeDirective_ImportURI(IncludeDirective model, Assignment assignment, ContentAssistContext context, ICompletionProposalAcceptor acceptor){
		super.completeIncludeDirective_ImportURI(model, assignment, context, acceptor) var String fileName=model.getImportURI() 
		var Resource resource=model.eResource() 
		if (resource != null) {
			acceptFileNameProposals(resource, context, acceptor, Arrays.asList("rst"), fileName) 
		}
		
	}
	
}