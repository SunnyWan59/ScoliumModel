import "./citation-styles";


/**
 * Converts raw metadata into structured CitationData format
 * @param rawMetadata Raw metadata object from source
 * @returns Formatted CitationData object
 */
function formatMetadata(rawMetadataList: any[]): CitationData[] {
  return rawMetadataList.map(rawMetadata => {
    // Extract and format authors
    const authors: Author[] = [];
    if (rawMetadata.authors) {
      rawMetadata.authors.forEach((author: string) => {
        // Handle cases where author name might be "LastName, FirstName" or "FirstName LastName"
        const nameParts = author.includes(',') 
          ? author.split(',').map(part => part.trim()).reverse()
          : author.split(' ');

        authors.push({
          firstName: nameParts[0] || '',
          lastName: nameParts[nameParts.length - 1] || ''
        });
      });
    }

    // Extract other citation fields with fallbacks
    return {
      authors,
      title: rawMetadata.title || '',
      publisher: rawMetadata.publisher || 'arXiv',
      year: rawMetadata.year?.toString() || ''
    };
  });
}


/**
 * Generates citations from metadata based on the specified citation style
 * @param metadata Array of citation metadata
 * @param style Citation style (APA, MLA, Chicago, Harvard, or Vancouver)
 * @returns Array of formatted citations
 */
function generateCitations(metadata: CitationData[], style: string): string[] {
  return metadata.map(data => {
    switch(style.toUpperCase()) {
      case "APA":
        return generateAPACitation(data);
      case "MLA": 
        return generateMLACitation(data);
      case "CHICAGO":
        return generateChicagoCitation(data);
      case "HARVARD":
        return generateHarvardCitation(data);
      case "VANCOUVER":
        return generateVancouverCitation(data);
      default:
        return generateAPACitation(data); // Default to APA if style not recognized
    }
  });
}

/**
 * Combines metadata extraction and citation generation into a single function
 * @param rawMetadata Array of raw metadata objects
 * @param style Citation style (APA, MLA, Chicago, Harvard, or Vancouver)
 * @returns Array of formatted citations
 */
export function processAndGenerateCitations(rawMetadata: any[], style: string): string[] {
  // First convert raw metadata into CitationData format
  const citationData = formatMetadata(rawMetadata);
  
  // Then generate citations in requested style
  return generateCitations(citationData, style);
}


