package rs.demsys.rst.ui.contentassist;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import com.google.inject.Inject;

import org.eclipse.core.resources.IContainer;
import org.eclipse.core.resources.IFile;
import org.eclipse.core.resources.IResource;
import org.eclipse.core.resources.IWorkspaceRoot;
import org.eclipse.core.resources.ResourcesPlugin;
import org.eclipse.core.runtime.CoreException;
import org.eclipse.core.runtime.IPath;
import org.eclipse.core.runtime.Path;
import org.eclipse.emf.common.util.URI;
import org.eclipse.emf.ecore.EObject;
import org.eclipse.emf.ecore.resource.Resource;
import org.eclipse.jface.text.contentassist.ICompletionProposal;
import org.eclipse.xtext.Assignment;
import org.eclipse.xtext.RuleCall;
import org.eclipse.xtext.nodemodel.INode;
import org.eclipse.xtext.nodemodel.util.NodeModelUtils;
//import org.eclipse.xtext.resource.IContainer;
//import org.eclipse.xtext.resource.IResourceDescription;
//import org.eclipse.xtext.resource.IResourceDescriptions;
//import org.eclipse.xtext.resource.IResourceServiceProvider;
import org.eclipse.xtext.resource.impl.ResourceDescriptionsProvider;
import org.eclipse.xtext.ui.PluginImageHelper;
import org.eclipse.xtext.ui.editor.StatefulResourceDescription;
import org.eclipse.xtext.ui.editor.contentassist.ContentAssistContext;
import org.eclipse.xtext.ui.editor.contentassist.ICompletionProposalAcceptor;

import rs.demsys.rst.rst.IncludeDirective;

/** 
 * See https://www.eclipse.org/Xtext/documentation/304_ide_concepts.html#content-assist
 * on how to customize the content assistant.
 */
public class RstProposalProvider extends AbstractRstProposalProvider {
	
	@Inject private PluginImageHelper imageHelper;
	
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

	private static void recursiveFindProposals(ArrayList<String> fileProp, ArrayList<String> folderProp, List<String> exts, String fileName, IPath path, IWorkspaceRoot myWorkspaceRoot){
	    IContainer  container =  myWorkspaceRoot.getContainerForLocation(path);

	    try {
	        IResource[] iResources;
	        iResources = container.members();
	        for (IResource iR : iResources){
	            // for c files
	        	
	        	
	        	IPath irPath = iR.getFullPath();
	        	String resRelative = irPath.toString();
				
				resRelative = resRelative.substring(resRelative.indexOf("/", resRelative.indexOf("/") + 1) + 1);
				
				boolean resContainsFileName = false;
				boolean fileNameContainsRes = false;
				
				if (fileName == null)
				{
					resContainsFileName = true;
					fileNameContainsRes = false;
				}
				else
				{
					resContainsFileName = (resRelative.indexOf(fileName) == 0);
					fileNameContainsRes = (fileName.indexOf(resRelative) == 0);	
				}
				
	        	if (iR.getType() == IResource.FOLDER){
	        		if (resContainsFileName)
	        		{
	        			folderProp.add(resRelative);
	        		}
	        		else if (fileNameContainsRes)
	        		{
		                recursiveFindProposals(fileProp, folderProp, exts, fileName, iR.getLocation(), myWorkspaceRoot);	
	        		}
	            }
	        	else if (resContainsFileName)
	        	{
	        		for (String ext : exts)
		        	{
		        		if (ext.equalsIgnoreCase(iR.getFileExtension()))
		        		{
		        			fileProp.add(resRelative);
		        			break;
		        		}
		        	}
	        	}
	            
	        }
	    } catch (CoreException e) {
	        // TODO Auto-generated catch block
	        e.printStackTrace();
	    }
	}
	
	public void complete_IncludeDirective(EObject model, RuleCall ruleCall, ContentAssistContext context, ICompletionProposalAcceptor acceptor) {
		super.complete_IncludeDirective(model, ruleCall, context, acceptor);
	}
	
	public void completeIncludeDirective_ImportURI(IncludeDirective model, Assignment assignment, 
			ContentAssistContext context, ICompletionProposalAcceptor acceptor) {
		
//		INode node = NodeModelUtils.findActualNodeFor(model.getImportURI());
		
		String fileName = model.getImportURI(); //node.getText();
		
		super.completeIncludeDirective_ImportURI(model, assignment, context, acceptor);
		
		Resource resource = model.eResource();
		
		if (resource != null) {
			
			String platformString = resource.getURI().toPlatformString(true);
			IFile curFile = ResourcesPlugin.getWorkspace().getRoot().getFile(new Path(platformString));
			
			String prjName = curFile.getProject().getFullPath().toString();
			
			
			ArrayList<String> fileProp = new ArrayList<String>(); 
			ArrayList<String> folderProp = new ArrayList<String>();
			
			recursiveFindProposals(fileProp, folderProp, Arrays.asList("rst"), fileName, 
					curFile.getProject().getLocation(), ResourcesPlugin.getWorkspace().getRoot());
			
			for (String f : folderProp)
			{
				
				ICompletionProposal proposal = createCompletionProposal(f + "/", 
						f, 
						imageHelper.getImage("folder.gif"),
						context);
				acceptor.accept(proposal);
			}
			
			for (String f : fileProp)
			{
				ICompletionProposal proposal = createCompletionProposal(f, 
						f, 
						imageHelper.getImage("rst_file.png"),
						context);
				acceptor.accept(proposal);
			}
			
//			IResourceDescription.Manager mngr = getManager(resource);
//			IResourceDescriptions index = resourceDescriptionsProvider
//					.createResourceDescriptions();
//
//			IResourceDescription descr = mngr.getResourceDescription(resource);
//
//			for (IContainer visibleContainer : manager.getVisibleContainers(
//					descr, index)) {
//				for (IResourceDescription visibleResourceDesc : visibleContainer
//						.getResourceDescriptions()) {
//
//					if (! (visibleResourceDesc instanceof StatefulResourceDescription))
//					{
//						String resRelative = visibleResourceDesc.getURI().toPlatformString(false);
//						
//						resRelative = resRelative.substring(resRelative.indexOf("/", resRelative.indexOf("/") + 1) + 1);
//						
//						if(resRelative.indexOf(fileName) == 0)
//						{
//							ICompletionProposal proposal = createCompletionProposal(
//									resRelative,
//									context);
//							acceptor.accept(proposal);
//						}
//					}
////					System.out.println(visibleResourceDesc);
//				}
//		
//			}
	
	
		}
	}
		
//		var Resource resource = use.eResource()
//		if (resource != null) {
//			var String importedNamespace = use.getImportedNamespace()
//			var IResourceDescription.Manager mngr = getManager(resource)
//			var IResourceDescriptions index = resourceDescriptionsProvider.createResourceDescriptions()
//			var IResourceDescription descr = mngr.getResourceDescription(resource)
//			for (IContainer visibleContainer : manager.getVisibleContainers(descr, index)) {
//				for (IResourceDescription visibleResourceDesc : visibleContainer.getResourceDescriptions()) {
//					var Iterable<IEObjectDescription> exportedObject = visibleResourceDesc.getExportedObjects()
//					if (exportedObject != null) {
//						for (IEObjectDescription ieObjectDescription : exportedObject) {
//							if (ieObjectDescription != null) {
//								var QualifiedName qualifiedName = ieObjectDescription.getQualifiedName()
//								if (qualifiedName != null) {
//									var String[] imports = (#[] as String[])
//									var boolean addSegment = false
//									if (importedNamespace != null) {
//										importedNamespace = importedNamespace.trim()
//										imports = importedNamespace.split("\\.")
//										addSegment = importedNamespace.endsWith(".") || importedNamespace.equals("")
//									} else {
//										addSegment = true
//									}
//									var int segmentsCount = imports.length
//									if (addSegment) {
//										segmentsCount++
//									}
//									if (qualifiedName.getSegmentCount() == segmentsCount) {
//										var boolean ok = true
//										if (importedNamespace != null && !importedNamespace.equals("")) {
//											ok = startsWith(qualifiedName, converter.toQualifiedName(importedNamespace),
//												true)
//										}
//										if (ok) {
//											var ICompletionProposal proposal = createCompletionProposal(
//												qualifiedName.toString(), context)
//											acceptor.accept(proposal)
//										}
//
//									}
//
//								}
//
//							}
//
//						}
//
//					}
//
//				}
//
//			}
//
//		}

	//}

//}

}
