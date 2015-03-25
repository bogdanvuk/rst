package rs.demsys.rst.ui.contentassist;

import com.google.inject.Inject;

import org.eclipse.core.resources.IFile;
import org.eclipse.core.resources.ResourcesPlugin;
import org.eclipse.core.runtime.Path;
import org.eclipse.emf.common.util.URI;
import org.eclipse.emf.ecore.EObject;
import org.eclipse.emf.ecore.resource.Resource;
import org.eclipse.jface.text.contentassist.ICompletionProposal;
import org.eclipse.xtext.Assignment;
import org.eclipse.xtext.RuleCall;
import org.eclipse.xtext.nodemodel.INode;
import org.eclipse.xtext.nodemodel.util.NodeModelUtils;
import org.eclipse.xtext.resource.IContainer;
import org.eclipse.xtext.resource.IResourceDescription;
import org.eclipse.xtext.resource.IResourceDescriptions;
import org.eclipse.xtext.resource.IResourceServiceProvider;
import org.eclipse.xtext.resource.impl.ResourceDescriptionsProvider;
import org.eclipse.xtext.ui.editor.StatefulResourceDescription;
import org.eclipse.xtext.ui.editor.contentassist.ContentAssistContext;
import org.eclipse.xtext.ui.editor.contentassist.ICompletionProposalAcceptor;

import rs.demsys.rst.rst.IncludeDirective;

/** 
 * See https://www.eclipse.org/Xtext/documentation/304_ide_concepts.html#content-assist
 * on how to customize the content assistant.
 */
public class RstProposalProvider extends AbstractRstProposalProvider {
	
	@Inject
	private IContainer.Manager manager;

	@Inject
	private IResourceServiceProvider.Registry rspr;

	@Inject
	private ResourceDescriptionsProvider resourceDescriptionsProvider;

	private IResourceDescription.Manager getManager(Resource res) {
		IResourceServiceProvider resourceServiceProvider = rspr
				.getResourceServiceProvider(res.getURI());
		return resourceServiceProvider.getResourceDescriptionManager();
	}

	public void completeIncludeDirective_ImportURI(IncludeDirective model, Assignment assignment, 
			ContentAssistContext context, ICompletionProposalAcceptor acceptor) {
		
		INode node = NodeModelUtils.findActualNodeFor(model.getImportURI());
		
		String fileName = node.getText();
		
		super.completeIncludeDirective_ImportURI(model, assignment, context, acceptor);
		
		Resource resource = model.eResource();
		
		if (resource != null) {
			
			String platformString = resource.getURI().toPlatformString(true);
			IFile curFile = ResourcesPlugin.getWorkspace().getRoot().getFile(new Path(platformString));
			
			String prjName = curFile.getProject().getFullPath().toString();
			
			IResourceDescription.Manager mngr = getManager(resource);
			IResourceDescriptions index = resourceDescriptionsProvider
					.createResourceDescriptions();

			IResourceDescription descr = mngr.getResourceDescription(resource);

			for (IContainer visibleContainer : manager.getVisibleContainers(
					descr, index)) {
				for (IResourceDescription visibleResourceDesc : visibleContainer
						.getResourceDescriptions()) {

					if (! (visibleResourceDesc instanceof StatefulResourceDescription))
					{
						String resRelative = visibleResourceDesc.getURI().toPlatformString(false);
						
						resRelative = resRelative.substring(resRelative.indexOf("/", resRelative.indexOf("/") + 1) + 1);
						
						if(resRelative.indexOf(fileName) == 0)
						{
							ICompletionProposal proposal = createCompletionProposal(
									resRelative,
									context);
							acceptor.accept(proposal);
						}
					}
//					System.out.println(visibleResourceDesc);
				}
		
			}
	
	
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
