import { http, HttpResponse } from 'msw'
import { Skill, Command, Agent, SearchResult } from '@/types'
import { mockSkills, mockCommands, mockAgents } from './mockData'

export const handlers = [
  // Skills endpoints
  http.get('/api/skills', ({ request }) => {
    const url = new URL(request.url)
    const page = parseInt(url.searchParams.get('page') || '1')
    const pageSize = parseInt(url.searchParams.get('pageSize') || '20')
    const search = url.searchParams.get('search')
    const stage = url.searchParams.get('stage')

    let filtered = mockSkills

    if (search) {
      const query = search.toLowerCase()
      filtered = filtered.filter(
        skill =>
          skill.name.toLowerCase().includes(query) ||
          skill.description.toLowerCase().includes(query)
      )
    }

    if (stage) {
      filtered = filtered.filter(skill => skill.stage === stage)
    }

    const startIndex = (page - 1) * pageSize
    const endIndex = startIndex + pageSize
    const paginatedData = filtered.slice(startIndex, endIndex)

    return HttpResponse.json({
      data: paginatedData,
      pagination: {
        page,
        pageSize,
        totalItems: filtered.length,
        totalPages: Math.ceil(filtered.length / pageSize),
      },
    })
  }),

  http.get('/api/skills/:id', ({ params }) => {
    const { id } = params
    const skill = mockSkills.find(s => s.id === id)

    if (!skill) {
      return HttpResponse.json(
        { error: 'Not Found', message: 'Skill not found', code: 'NOT_FOUND' },
        { status: 404 }
      )
    }

    return HttpResponse.json({
      skill,
      related_skills: mockSkills.filter(s => s.stage === skill.stage && s.id !== skill.id).slice(0, 3),
      used_by_commands: [],
      used_by_agents: [],
    })
  }),

  // Commands endpoints
  http.get('/api/commands', ({ request }) => {
    const url = new URL(request.url)
    const page = parseInt(url.searchParams.get('page') || '1')
    const pageSize = parseInt(url.searchParams.get('pageSize') || '20')
    const search = url.searchParams.get('search')
    const stage = url.searchParams.get('stage')

    let filtered = mockCommands

    if (search) {
      const query = search.toLowerCase()
      filtered = filtered.filter(
        cmd =>
          cmd.name.toLowerCase().includes(query) ||
          cmd.description.toLowerCase().includes(query)
      )
    }

    if (stage) {
      filtered = filtered.filter(cmd => cmd.stage === stage)
    }

    const startIndex = (page - 1) * pageSize
    const endIndex = startIndex + pageSize
    const paginatedData = filtered.slice(startIndex, endIndex)

    return HttpResponse.json({
      data: paginatedData,
      pagination: {
        page,
        pageSize,
        totalItems: filtered.length,
        totalPages: Math.ceil(filtered.length / pageSize),
      },
    })
  }),

  http.get('/api/commands/:id', ({ params }) => {
    const { id } = params
    const command = mockCommands.find(c => c.id === id)

    if (!command) {
      return HttpResponse.json(
        { error: 'Not Found', message: 'Command not found', code: 'NOT_FOUND' },
        { status: 404 }
      )
    }

    return HttpResponse.json({
      command,
      invoked_skills: [],
      spawned_agents: [],
    })
  }),

  // Agents endpoints
  http.get('/api/agents', ({ request }) => {
    const url = new URL(request.url)
    const page = parseInt(url.searchParams.get('page') || '1')
    const pageSize = parseInt(url.searchParams.get('pageSize') || '20')
    const search = url.searchParams.get('search')
    const stage = url.searchParams.get('stage')

    let filtered = mockAgents

    if (search) {
      const query = search.toLowerCase()
      filtered = filtered.filter(
        agent =>
          agent.name.toLowerCase().includes(query) ||
          agent.description.toLowerCase().includes(query)
      )
    }

    if (stage) {
      filtered = filtered.filter(agent => agent.stage === stage)
    }

    const startIndex = (page - 1) * pageSize
    const endIndex = startIndex + pageSize
    const paginatedData = filtered.slice(startIndex, endIndex)

    return HttpResponse.json({
      data: paginatedData,
      pagination: {
        page,
        pageSize,
        totalItems: filtered.length,
        totalPages: Math.ceil(filtered.length / pageSize),
      },
    })
  }),

  http.get('/api/agents/:id', ({ params }) => {
    const { id } = params
    const agent = mockAgents.find(a => a.id === id)

    if (!agent) {
      return HttpResponse.json(
        { error: 'Not Found', message: 'Agent not found', code: 'NOT_FOUND' },
        { status: 404 }
      )
    }

    return HttpResponse.json({
      agent,
      loaded_skills: [],
      spawned_by_commands: [],
    })
  }),

  // Search endpoint
  http.get('/api/search', ({ request }) => {
    const url = new URL(request.url)
    const query = url.searchParams.get('query')
    const limit = parseInt(url.searchParams.get('limit') || '10')

    if (!query) {
      return HttpResponse.json({ results: [], total: 0 })
    }

    const queryLower = query.toLowerCase()
    const results: SearchResult[] = []

    // Search skills
    mockSkills
      .filter(
        skill =>
          skill.name.toLowerCase().includes(queryLower) ||
          skill.description.toLowerCase().includes(queryLower)
      )
      .forEach(skill => {
        results.push({
          id: skill.id,
          type: 'Skill',
          name: skill.name,
          description: skill.description,
          stage: skill.stage,
          score: 1.0,
        })
      })

    // Search commands
    mockCommands
      .filter(
        cmd =>
          cmd.name.toLowerCase().includes(queryLower) ||
          cmd.description.toLowerCase().includes(queryLower)
      )
      .forEach(cmd => {
        results.push({
          id: cmd.id,
          type: 'Command',
          name: cmd.name,
          description: cmd.description,
          stage: cmd.stage,
          score: 0.9,
        })
      })

    // Search agents
    mockAgents
      .filter(
        agent =>
          agent.name.toLowerCase().includes(queryLower) ||
          agent.description.toLowerCase().includes(queryLower)
      )
      .forEach(agent => {
        results.push({
          id: agent.id,
          type: 'Agent',
          name: agent.name,
          description: agent.description,
          stage: agent.stage,
          score: 0.8,
        })
      })

    // Sort by score and limit
    const sorted = results.sort((a, b) => b.score - a.score).slice(0, limit)

    return HttpResponse.json({ results: sorted, total: results.length })
  }),
]
