const events = [
  {
    title: 'Open-Air Konzert',
    date: '12. Juni 2026',
    location: 'Stadtpark',
    description: 'Ein Abend voller Musik unter freiem Himmel.'
  },
  {
    title: 'Sommerfest',
    date: '5. Juli 2026',
    location: 'Marktplatz',
    description: 'Bunte Stände, Spiele und leckeres Essen.'
  },
  {
    title: 'Strandvolleyball Turnier',
    date: '16. August 2026',
    location: 'Seebad',
    description: 'Teams treten am Strand gegeneinander an.'
  },
  {
    title: 'Herbstlicher Wandertag',
    date: '20. September 2026',
    location: 'Bergpfad',
    description: 'Wanderung durch die ersten Herbstfarben.'
  }
];

const container = document.getElementById('cards-container');

function createCard(event) {
  const card = document.createElement('div');
  card.className = 'card';

  card.innerHTML = `
    <h2>${event.title}</h2>
    <p><strong>Datum:</strong> ${event.date}</p>
    <p><strong>Ort:</strong> ${event.location}</p>
    <p>${event.description}</p>
  `;

  return card;
}

events.forEach(event => {
  const card = createCard(event);
  container.appendChild(card);
});
