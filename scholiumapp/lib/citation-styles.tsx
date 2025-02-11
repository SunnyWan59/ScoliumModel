// Define an interface for an author.
type Author = {
    firstName: string;
    lastName: string;
}
  
// Define an interface for the citation data.
type CitationData ={
    authors: Author[];
    title: string;
    publisher: string;
    year: number;
}
  
/* ===================== Helper Functions for Author Formatting ===================== */

/**
 * Formats authors for MLA style.
 * - One author: "Lastname, Firstname"
 * - Two authors: "Lastname, Firstname, and Firstname Lastname"
 * - Three or more: "Lastname, Firstname, et al."
 */
function formatAuthorsMLA(authors: Author[]): string {
    if (authors.length === 0) {
        return "";
    } else if (authors.length === 1) {
        const author = authors[0];
        return `${author.lastName}, ${author.firstName}`;
    } else if (authors.length === 2) {
        const [first, second] = authors;
        return `${first.lastName}, ${first.firstName}, and ${second.firstName} ${second.lastName}`;
    } else {
        const first = authors[0];
        return `${first.lastName}, ${first.firstName}, et al.`;
    }
}

/**
 * Formats authors for APA style.
 * Each author is formatted as "Lastname, F." (initial for each given name).
 * Authors are separated by commas, with an ampersand (&) before the final author.
 */
function formatAuthorsAPA(authors: Author[]): string {
    if (authors.length === 0) {
      return "";
    }
  
    const formattedAuthors = authors.map((author) => {
      const initials = author.firstName
        .split(" ")
        .map((name) => name.charAt(0) + ".")
        .join(" ");
      return `${author.lastName}, ${initials}`;
    });
  
    if (formattedAuthors.length === 1) {
      return formattedAuthors[0];
    } else if (formattedAuthors.length === 2) {
      return `${formattedAuthors[0]}, & ${formattedAuthors[1]}`;
    } else {
      const lastAuthor = formattedAuthors.pop();
      return `${formattedAuthors.join(", ")}, & ${lastAuthor}`;
    }
}
  
/**
 * Formats authors for Chicago style.
 * - One author: "Lastname, Firstname"
 * - Two authors: "Lastname, Firstname and Firstname Lastname"
 * - Three or more: First author inverted; subsequent authors in normal order,
 *   with commas and an "and" before the final name.
*/
function formatAuthorsChicago(authors: Author[]): string {
    if (authors.length === 0) {
      return "";
    }
  
    const formatted: string[] = [];
    authors.forEach((author, index) => {
      if (index === 0) {
        formatted.push(`${author.lastName}, ${author.firstName}`);
      } else {
        formatted.push(`${author.firstName} ${author.lastName}`);
      }
    });
  
    if (formatted.length === 1) {
      return formatted[0];
    } else if (formatted.length === 2) {
      return formatted.join(" and ");
    } else {
      return formatted.slice(0, -1).join(", ") + ", and " + formatted[formatted.length - 1];
    }
}
  
/**
 * Formats authors for Harvard style.
 * - One to three authors: list all authors formatted as "Lastname, F."
 *   and joined with "and" before the final author.
 * - More than three authors: list the first author followed by "et al."
 */
function formatAuthorsHarvard(authors: Author[]): string {
    if (authors.length === 0) {
      return "";
    }
  
    const formatName = (author: Author) => {
      const initials = author.firstName
        .split(" ")
        .map((name) => name.charAt(0) + ".")
        .join(" ");
      return `${author.lastName}, ${initials}`;
    };
  
    if (authors.length === 1) {
      return formatName(authors[0]);
    } else if (authors.length <= 3) {
      const formatted = authors.map(formatName);
      if (formatted.length === 2) {
        return formatted.join(" and ");
      } else {
        // For three authors, join first two with commas and add ", and" before the last.
        return `${formatted.slice(0, -1).join(", ")}, and ${formatted[formatted.length - 1]}`;
      }
    } else {
      // More than three authors: use first author followed by "et al."
      return `${formatName(authors[0])} et al.`;
    }
  }
  
  /**
   * Formats authors for Vancouver style.
   * Authors are formatted as "Lastname Initials" (with no punctuation between initials)
   * and separated by commas. If there are more than 6 authors, list the first 6 followed by "et al."
   */
  function formatAuthorsVancouver(authors: Author[]): string {
    if (authors.length === 0) {
      return "";
    }
  
    // If more than 6 authors, list only the first 6.
    let authorsToFormat = authors;
    if (authors.length > 6) {
      authorsToFormat = authors.slice(0, 6);
    }
  
    const formatted = authorsToFormat.map((author) => {
      // Combine initials without spaces.
      const initials = author.firstName.split(" ").map(n => n.charAt(0)).join("");
      return `${author.lastName} ${initials}`;
    });
  
    let result = formatted.join(", ");
    if (authors.length > 6) {
      result += ", et al.";
    }
    return result;
}
  
/* ===================== Citation Generator Functions ===================== */

/**
 * Generates a citation in MLA format.
 * Example: "Doe, John, et al. Understanding TypeScript. Tech Books Publishing, 2023."
 */
function generateMLACitation(data: CitationData): string {
    const authors = formatAuthorsMLA(data.authors);
    return `${authors}. ${data.title}. ${data.publisher}, ${data.year}.`;
}

/**
 * Generates a citation in APA format.
 * Example: "Doe, J., & Smith, J. (2023). Understanding TypeScript. Tech Books Publishing."
 */
function generateAPACitation(data: CitationData): string {
    const authors = formatAuthorsAPA(data.authors);
    return `${authors} (${data.year}). ${data.title}. ${data.publisher}.`;
}

/**
 * Generates a citation in Chicago format.
 * Example: "Doe, John, Jane Smith, and Emily Johnson. Understanding TypeScript. Tech Books Publishing, 2023."
 */
function generateChicagoCitation(data: CitationData): string {
    const authors = formatAuthorsChicago(data.authors);
    return `${authors}. ${data.title}. ${data.publisher}, ${data.year}.`;
}

/**
 * Generates a citation in Harvard format.
 * Example (for up to three authors):
 * "Doe, J. and Smith, J. (2023) Understanding TypeScript. Tech Books Publishing."
 * For more than three authors, only the first author is shown followed by "et al."
 */
function generateHarvardCitation(data: CitationData): string {
    const authors = formatAuthorsHarvard(data.authors);
    return `${authors} (${data.year}) ${data.title}. ${data.publisher}.`;
}

/**
 * Generates a citation in Vancouver format.
 * Example: "Doe J, Smith J, Johnson E. Understanding TypeScript. Tech Books Publishing; 2023."
 */
function generateVancouverCitation(data: CitationData): string {
    const authors = formatAuthorsVancouver(data.authors);
    return `${authors}. ${data.title}. ${data.publisher}; ${data.year}.`;
}
  
  /* ===================== Example Usage ===================== */
  
  const citationData: CitationData = {
    authors: [
      { firstName: "John", lastName: "Doe" },
      { firstName: "Jane", lastName: "Smith" },
      { firstName: "Emily",lastName: "Johnson" },
      // Uncomment the next line to test more than three authors in Harvard style
      // { firstName: "Robert", lastName: "Brown" },
    ],
    title: "Understanding TypeScript",
    publisher: "Tech Books Publishing",
    year: 2023,
  };
  
  console.log("MLA Citation:");
  console.log(generateMLACitation(citationData));
  console.log("\nAPA Citation:");
  console.log(generateAPACitation(citationData));
  console.log("\nChicago Citation:");
  console.log(generateChicagoCitation(citationData));
  console.log("\nHarvard Citation:");
  console.log(generateHarvardCitation(citationData));
  console.log("\nVancouver Citation:");
  console.log(generateVancouverCitation(citationData));