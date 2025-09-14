const events = [
  {
    title: 'Big Knock',
    date: 't.b.a.',
    location: 'Somewhere in England',
    description: 'Ein Abend voller Musik unter freiem Himmel.'
  },
  {
    title: 'Bergrennen Gaschney',
    date: '5. Juli 2026',
    location: 'In den Vogesen',
    description: 'Bunte Stände, Spiele und leckeres Essen.'
  },
  {
    title: 'Sommer Dieseltreffen',
    date: '16. August 2026',
    location: 'Geyern',
    description: 'Teams treten am Strand gegeneinander an.'
  },
  {
    title: 'Internationales Dieselmotorradtreffen',
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
